#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask
from flask import render_template
from flask import jsonify, make_response
from flask import request
import nltk
import random
import re
import snowballstemmer
from confs import CCF_CONF 
from nltk import word_tokenize
from nltk.corpus import stopwords
# from utils import getRe, getRe2
from pymongo import MongoClient
from flask_cors import CORS
from flask_cache import Cache
import time
from nltk.stem import WordNetLemmatizer
cache = Cache(config={'CACHE_TYPE': 'simple'}, with_jinja2_ext=False)
app = Flask(__name__)
cache.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
#Client = MongoClient("mongodb://dev_read:dev_read@166.111.139.42")
Client = MongoClient("mongodb://root_esoda:root_esoda@127.0.0.1")
col = Client.hcihub.esoda_hci_papers
wlem = WordNetLemmatizer()
@app.route('/')
@app.route('/index')
def index():
    return '/search/ + your query(eg:"?conf=CHI")'



def get_lemma(text):
    l_url = "http://localhost:9000/?properties={'annotators': 'lemma', 'pipelinelanguage': 'en', 'outputFormat': 'json'}"
    lemma = requests.post(l_url, text.encode('utf-8'), timeout = 5).text
    return json.loads(lemma)['sentences']


def get_lemma_snowball(word):
    '''
    input : words (list or string(single word))
    output: words (list)
    '''
    temp = []
    if isinstance(word, list):
        temp = word
    else:
        temp.append(word)
    stemmer = snowballstemmer.stemmer('english');
    return stemmer.stemWords(temp)
    

@cache.memoize(600)
def get_stems(text):
    stems = []
    lemma = get_lemma(text)
    for sen in lemma:
        for word in sen['tokens']:
            stems.append(word['lemma'])
    return list(set(stems))

    

def modifyResult(stems, result):
    #wlem = WordNetLemmatizer()
    color_list = ["#B5CAFF", "#B9B9B9"]
    score = 0
    shift = 0
    span_r = 26 + 7
    span_l = 7
    lemma = get_lemma(result)
    stems = get_lemma_snowball(stems)
    for sen in lemma:
        for word in sen['tokens']:
            lemma_snowball = get_lemma_snowball(word['lemma'].lower())[0]
            if lemma_snowball in stems:
                cnt = stems.index(lemma_snowball) % len(color_list)
                score += 1
                result = result[:shift+word['characterOffsetBegin']] + \
                         '<span style="background:%s">'%color_list[cnt] + \
                         result[shift+word['characterOffsetBegin']:]
                shift += span_r
                result = result[:shift+word['characterOffsetEnd']] + \
                         '</span>' + \
                         result[shift+word['characterOffsetEnd']:] 
                shift += span_l
                continue
            for temp in lemma_snowball.split('-'): 
            # 为了让finger-aware也能匹配到aware，所以finger-aware要能匹配三个['finger-aware', 'finger', 'aware']
                if temp in stems:
                    cnt = stems.index(temp) % len(color_list)
                    score += 1
                    result = result[:shift+word['characterOffsetBegin']] + \
                             '<span style="background:%s">'%color_list[cnt] + \
                             result[shift+word['characterOffsetBegin']:]
                    shift += span_r
                    result = result[:shift+word['characterOffsetEnd']] + \
                             '</span>' + \
                             result[shift+word['characterOffsetEnd']:] 
                    shift += span_l
                    break
    return result, score
    
    
def modify_res(stems, item):
    item['title'],title_score = modifyResult(stems, item['title'])
    item['summary'], summary_score = modifyResult(stems, item['summary'])
    return item





#@cache.memoize(600)
def get_res(query,years,confs,authors, skip, sort_type):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    filtered_query = [w for w in word_tokens if not w in stop_words]
    # print(filtered_query)
    stems = get_stems(' '.join(filtered_query))
    # print(stems)
    resList = []
    con = []
    que_str = ''
    for que in stems:
        que_str += '"' + que + '" '
    con.append({'$text':{'$search':que_str}})
    if years != None and years != []:
        con.append({'year': {'$in': years}})
    if confs != None:
        confs = [x.strip().split(':')[0] for x in confs]
    if confs != None and confs != []:
        con.append({'shortName': {'$in': confs}})
    if authors != None and authors != []:
        con.append({'authors.name': {'$in': authors}})
    
    
    # print('con',con)
    
    
    res = {}
    res['authors'] = col.distinct('authors.name', {'$and': con})
    res['years'] = col.distinct('year', {'$and': con})
    res['confs'] = list(col.aggregate([{'$match': {'$and': con}}, {'$group': {'_id': '$shortName', 'cnt':{'$sum':1}}}]))    
    res['num'] = col.find({'$and': con}).count()
    
    limit = 10
    score = sort_type
    if score == 1:
        pip = [
            { '$match' : {'$and': con} },
            # { '$addFields' : {'yearInt' : { '$convert': {'input': '$year', 'to': 'int', 'onError': 0, 'onNull': 0}}}},
            # { '$addFields' : {'yearInt' : year}},
            #{ '$addFields' : {'score': {'$sum': [{'$meta': 'textScore'}]}}},

            # { '$project' : { '_id': 0, 'score': {'$sum': [{'$subtract': ["$yearInt", 2018]}, { '$meta': 'textScore' } ]}}},
            { '$sort' : { 'score': { '$meta': "textScore" }}},
            { '$skip' : skip },
            { '$limit' : limit},
            { '$project': {'_id': 0, 'title': 1, 'url': 1,'summary': 1, 'lemma_str': 1, 'shortName': 1, 'year': 1, 'authors': 1}}
        ]
    elif score == 2:
        pip = [
            { '$match' : {'$and': con} },
            { '$sort' : {'yearInt': -1, 'score': { '$meta': "textScore" }}},
            { '$skip' : skip },
            { '$limit' : limit},
            { '$project': {'_id': 0, 'title': 1, 'url': 1, 'summary': 1, 'lemma_str': 1, 'shortName': 1, 'year': 1, 'authors': 1}}
        ]
    else: #score=3
        pip = [
            { '$match' : {'$and': con} },
            # { '$group': {'_id': '$shortName', 'title': {'$addToSet': '$title'},'cnt':{'$sum':1}}},
            { '$sort' : {'cnt': -1 }},
            { '$skip' : skip },
            { '$limit' : limit},
            # { '$project': {'_id': 0, 'title': 1, 'summary': 1, 'lemma_str': 1, 'shortName': 1}}
        ]

    res['reslist'] = list(col.aggregate(pip))
    res['confs'] = sorted(res['confs'], key=lambda x: x['cnt'], reverse=True)
    res['ccf_confs'] = res['confs'][:20]
    try:
        res['confs'] = res['confs'][20:]
    except:
        res['confs'] = []
    res['years'] = sorted(res['years'], reverse=True)
    res['authors'] = sorted(res['authors'], reverse=True)[:100]
    # print( type(res))
    res['reslist'] = list(map(lambda x: modify_res(stems, x), res['reslist']))

    return res


@app.route('/search_post/', methods=['GET', 'POST', 'OPTIONS']) # 都用这个
def post_api():
    tmp = time.time()
    if request.method == 'GET':
        query = request.args.get('query') # aim for title and summary
        years = request.args.get('year')
        confs = request.args.get('conf')
        authors = request.args.get('author')
        index = request.args.get('index')
    elif request.method == 'OPTIONS':
        print('options')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'content-type'
            }
        response = make_response((jsonify({'error_code': 0}), 200, headers)) 
        return response
    else:
        print('post')
        data = request.get_json()
        query = data['query']
        print(query)
        years = data['year']
        sort_type = data['sort']
        try:
            confs = data['conf']
        except:
            confs = []
        authors = data['authors']
        index=data['index']
    #print(query,years,confs,authors)
    print('before_search', time.time()-tmp)
    tmp = time.time()
    resList = get_res(query,years,confs,authors,(int(index)-1)*10, sort_type)
    print('search_time',time.time()-tmp )
    tmp = time.time()
    response = jsonify({'result':resList})
    response.headers.add('Access-Control-Allow-Origin', '*')
    print('return', request.method)
    print('all_time',time.time()-tmp )
    return response
def get_res_for_citation(query):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    filtered_query = [w for w in word_tokens if not w in stop_words]
    stems = get_stems(' '.join(filtered_query))
    resList = []
    con = []
    que_str = ''
    for que in stems:
        que_str += '"' + que + '" '
    con.append({'$text':{'$search':que_str}})
    if years != None and years != []:
        con.append({'year': {'$in': years}})
    if confs != None:
        confs = [x.strip().split(':')[0] for x in confs]
    if confs != None and confs != []:
        con.append({'shortName': {'$in': confs}})
    if authors != None and authors != []:
        con.append({'authors.name': {'$in': authors}})
    pip = [
        { '$match' : {'$and': con} },
    ]

    res = list(col.aggregate(pip))
    nodes = []
    for x in res:
        if 'acmdl_id' in x:
            if len(x['acmdl_id'].strip()):
                nodes.append(x['acmdl_id'].strip())


    return nodes


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
