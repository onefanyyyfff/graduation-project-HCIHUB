import networkx as nx
from pymongo import MongoClient
from networkx.algorithms import community
from utils_for_graph import get_res_for_citation
from node2vec import Node2Vec
import time
from sklearn.cluster import KMeans
import pdb
class QuickFind(object):
    def __init__(self,nodes):
        self.count = len(nodes)
        self.id = {}
        for node in nodes:
            self.id[node] = node

    def connected(self,p,q):
        return self.find(p) == self.find(q)

    def find(self,p):
        if p != self.id[p]:
            self.id[p] = self.find(self.id[p])
            return self.id[p]
        else:
            return p

    def union(self,p,q):
        idp = self.find(p)
        idq = self.find(q)
        if idp != idq:
            self.id[idp] = idq
            self.count -= 1
    def compress(self):
        for i in self.id:
            self.find(i)


class CitationNetwork():
    def __init__(self, pair_file):
        nodes = {}
        edges = {}
        self.titles = {} 
        with open(pair_file, 'r') as f:
            for line in f:
                items = line.strip().split('|||')
                title = items[0]
                items = items[1].strip().split(' ')
                head = int(items[0])
                self.titles[head] = title
                nodes[head] = 1
                edges[head] = []
                for item in items[1:]:
                    try:
                        edges[head].append(int(item))
                    except:
                        pass
        self.nodes = nodes
        self.edges = edges
        #self.model = self.cluster(self.nodes.keys())
        
    def sub_graph(self, nodes):
        nodes = {int(x) for x in nodes}
        G = nx.DiGraph()
        for node in nodes:
            if not G.has_node(node):
                G.add_node(node)
            for nei in self.edges[node]:
                if not G.has_node(nei):
                    G.add_node(nei)
                G.add_edge(node, nei)
        return G
    def cluster_tool(self, nodes, num):
        vecs = []
        num_clusters = 3
        
        for node in nodes:
            vecs.append(self.model.wv[node])
        km_cluster = KMeans(n_clusters=num_clusters)
        result = km_cluster.fit_predict(vecs)
        return result
        
    def cluster(self, nodes, k=4):
        print('ori_node', len(nodes))
        graph = self.sub_graph(nodes)
        print('graph_nodes', len(graph))
        print('graph_edges', graph.size())
        node2vec = Node2Vec(graph, dimensions=64, walk_length=80, num_walks=len(graph)*2, workers=4)
        print('fitting')
        t1 = time.time()
        model = node2vec.fit(window=5, min_count=1, batch_words=4)
        print('fitting done, time:', time.time()-t1)
        num_clusters = k
        vecs = []
        for node in nodes:
            vecs.append(model.wv[node])
        km_cluster = KMeans(n_clusters=num_clusters)
        result = km_cluster.fit_predict(vecs)
        lists = []
        for id,node in zip(result, nodes):
            lists.append([id, self.titles[int(node)]])
        lists = sorted(lists, key = lambda x: x[0])
        with open('result.txt', 'w') as f:
            for x in lists:
                print(x, file=f)
        
cn = CitationNetwork('/root/hcihub/backend/pairs.txt')
cn.cluster(get_res_for_citation('brain machine interface'))
