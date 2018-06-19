# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 17:51:17 2018
@author: Moc
"""
#import numpy as np
import networkx as nx
#import matplotlib.pyplot as plt
#import pylab
#import time

#边节点转化成路口名称的形式
def NameEdge(list_all, list_result):
    list_all_op = []
    for result in list_result:
        for item in list_all:
            if result == item[1]:
                name = item[0]
                if name not in list_all_op:
                    list_all_op.append(name)
    return list_all_op

#判断边所在的线路， 判断属于那一条线路， 从而能够确定换乘的情况
def LineMoveOn(result_edges, edge1_list,edge2_list,edge3_list,edge4_list,edge5_list,edge7_list,edge9_list,edge11_list):
    line_list = []
    for item in result_edges:
        if item in edge1_list:
            line_list.append((item,'1号线'))
        elif item in edge2_list:
            line_list.append((item, '2号线'))
        elif item in edge3_list:
            line_list.append((item, '3号线'))
        elif item in edge4_list:
            line_list.append((item, '4号线'))
        elif item in edge5_list:
            line_list.append((item, '5号线'))
        elif item in edge7_list:
            line_list.append((item, '7号线'))
        elif item in edge9_list:
            line_list.append((item, '9号线'))
        elif item in edge11_list:
            line_list.append((item, '11号线'))
    print(line_list)
    return line_list           
    
class BestPath(): 
    #获取所有始发和重点能联通的路径       
    def ShortestPathGet(self, list_all, G, dict_all_edge, start, target):
        path = nx.all_simple_paths(G, source=start, target=target)
        list_all_path = []
        list_all_path_re = []
        for item in list(path):
            list_it = []
            list_it_re = []
            count = 0
            for it in range(len(item)):
                try:
                    edge = (item[it], item[it+1])
                    list_it.append(edge)
                    weight_edge = dict_all_edge[edge]
                    count += weight_edge
                    edge_re = (self.NameReplace(list_all, item[it]), self.NameReplace(list_all, item[it+1]))
                    list_it_re.append(edge_re)
                except:
                    pass
            list_all_path.append([list_it, count])
            list_all_path_re.append([list_it_re, count])
        return list_all_path, list_all_path_re
    
    #对路径的优劣进行排序，根据设置的权重
    def ShortedPathShow(self, list_all, G, dict_all_edge, start, target):
        list_all_path, list_all_path_re = self.ShortestPathGet(list_all, G, dict_all_edge, start, target)
        A = [(x[1], i, x) for i, x in enumerate(list_all_path)]
        A.sort()
        L = [s[2] for s in A]
        print(('节点 %d 到节点 %g 的所有路径, 推荐排序结果前三的路径：'%(start, target)))
        if len(L) >3:
            for list_i in L[:3]:
                print( list_i[0], list_i[1])
        else:
            for list_i in L:
                print( list_i[0], list_i[1])
        print('最优路线：', '\n', L[0][0])
        print('预计时间：','\n', L[0][1], 'min')
#        最短路径方法   快速！！！
#        path2=nx.dijkstra_path(G, source=start, target=target)
#        print('节点 %d 到 %g 的路径：' %(start, target), path2)
        return L[0][0]

#   节点格式转换， 字符转数字， 数字转字符， 需要转换才使用
    def NameReplace(self, list_all, node):
        if type(node) is str:
            for item in list_all:
                if node == item[0]:
                    node_re = item[1]
                if node == item[1]:
                    node_re = item[0]
        elif type(node) is int:
            for item in list_all:
                if node == item[1]:
                    node_re = item[0]
                if node_re == item[0]:
                    node_re = item[1]
        else:
            print('TYPE ERROR')
        return node_re

    #起始位置确定
    def StartLocation(self, list_all, edge):
        edge_re = (self.NameReplace(list_all, edge[0]), self.NameReplace(list_all, edge[1]))
        start_num = edge_re[0]
        return start_num
            
#if __name__ == '__main__':
#    start_time = time.clock()
#    B = BestPath()
#    G, dict_all_edge = BuildNetwok()
#    list_all = OriginMsg()
#    edge = ('a','b')
#    target =  'g'
#    start = B.StartLocation(list_all, edge)
#    target_re = B.NameReplace(list_all, target)
#    result = B.ShortedPathShow(list_all, G, dict_all_edge, start, target_re)
#    print('给网路设置布局...')
#    pos=nx.shell_layout(G)
#    print('画出网络图像：')
#    nx.draw(G,pos,with_labels=True, node_color='white', edge_color='b', node_size=400, width=3, alpha=0.5, style='dashed')
#    nx.draw(G,pos,with_labels=True, edgelist = result, node_color='white', edge_color='r',width=3, node_size=400, alpha=0.5)
#    pylab.title('Line Map Net',fontsize=15)
#    pylab.show()
#    end_time = time.clock()
#    time = end_time - start_time
#    print('time: %g s' %time)