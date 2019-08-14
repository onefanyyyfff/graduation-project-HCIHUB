# -*- coding:utf-8 -*-

import re
from nltk.stem import WordNetLemmatizer
wlem = WordNetLemmatizer()
def getRe(arr):
    '''
    用于正则表达式，便于数据库查询
    :param arr: 单个数据查询
    :return: 查询该数据的正则
    '''
    if arr is None:
        res = r'[\s\S]*'
    else:
        res = '^' + str(arr) + '$'
    return res

def getRe2(arrays):
    '''
    用于正则表达式，便于数据库查询
    :param arrays: 查询的是一个数据数组
    :return: 查询该数据数组的正则
    '''
    if arrays == [] or arrays is None:
        res = r'[\s\S]*'
    else:
        res = ["^" + str(x.strip().split(':')[0]) + "$" for x in arrays]
            
        #for arr in arrays[:-1]:
        #    
        #   res += "^" + str(arr) + "$" + '|'
        #res += "^" + str(arrays[-1]) + "$"
        res = '|'.join(res)
    return res

#def modifyResult(filtered_query, result):
#    '''
#    用来在title和summary中插入颜色
#    :param filtered_query: 用户输入的查询词
#    :param result: title 或者 summary
#    :return: 带有颜色标签的title 或 summary
#    '''
#    cnt = 0
#    color_list = ["#FFFF00", "#99FF99", "#99FFFF", "#FF99FF", "#FF9999"]
#    score=0
#    for word in filtered_query:
#        color_word = '<span style="background:%s">' % color_list[cnt] + word.lower() + '</span>'
#        cnt += 1
#        cnt %= len(color_list)
#        # result = result.replace(word, color_word)
#        result = re.sub(word, color_word, result, flags=re.IGNORECASE)
#        score+=len(re.findall(word,result,flags=re.IGNORECASE))
#    return result,score
def modifyResult(stems, result):
    #wlem = WordNetLemmatizer()
    cnt = 0
    color_list = ["#FFFF00", "#99FF99", "#99FFFF", "#FF99FF", "#FF9999"]
    score = 0
    res = []
    for word in result.strip().split(' '):
        stem = wlem.lemmatize(word)
        if stem in stems:
            score += 1
            cnt = stems.index(stem) % len(color_list)
            if word[-1] < 'A':
                res.append('<span style="background:%s">'%color_list[cnt]+word[:-1].lower()+word[-1]+'</span>')
            else:
                res.append('<span style="background:%s">'%color_list[cnt]+word.lower()+'</span>')
        else:
            res.append(word)
    return ' '.join(res), score
def modify_res(stems, item):
    #res = {}
    #res['score'] = 0
    item['title'],title_score = modifyResult(stems, item['title'])
    #res['score'] += title_score
    item['summary'], summary_score = modifyResult(stems, item['summary'])
    #res['score'] += summary_score
    #res['date'] = item['year']
    #try:
    #    res['score'] -= (2018-int(item['date']))//5
    #    res['score'] += int(item['date'])/2019
    #except:
    #    pass
    #res['conf'] = item['shortName']
    #res['authors'] = item['authors']
    return item
    
       
