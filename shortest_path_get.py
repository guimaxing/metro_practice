# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:00:08 2018
@author: Moc
"""
import numpy as np
import networkx as nx
#import matplotlib.pyplot as plt
import pylab


row=np.array([0,0,0,1,2,3,6,1])
col=np.array([1,2,3,4,5,6,7,6])
value=np.array([1,2,1,8,1,3,5,4])

G=nx.DiGraph()
print('为这个网络添加节点...')
for i in range(0,np.size(col)+1):
    G.add_node(i)
print('在网络中添加带权中的边...')
for i in range(np.size(row)):
    print([(row[i],col[i],value[i])])
    G.add_weighted_edges_from([(row[i],col[i],value[i])])
#
print('给网路设置布局...')
pos=nx.shell_layout(G)
print('画出网络图像：')
nx.draw(G,pos,with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5 )
pylab.title('Self_Define Net',fontsize=15)
pylab.show()
start = 1
end = 7

path=nx.dijkstra_path(G, source=start, target=end)
#for i in range(len(path)):
#    try:
#        aa = [dict_all[path[i]], dict_all[path[i+1]]]
#        print(aa)       
#    except:
#        pass        
print('节点 %d 到 %g 的路径：' %(start, end), path)
#print('节点 %d 到节点 %g 的所有路径：'%(start, end))

for (i, v) in G.edges():
    edge = (i,v)
    #    weight = k
    print(edge)