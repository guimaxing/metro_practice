# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:48:35 2018
@author: Moc
"""

from openpyxl import load_workbook
import networkx as nx
import time
from ForRoadMap import BestPath, NameEdge, LineMoveOn
import matplotlib.pyplot as plt
#import pylab

#载入数据，
def ReadData(path):
    edge1_list = []
    edge2_list = []
    edge3_list = []
    edge4_list = []
    edge5_list = []
    edge7_list = []
    edge9_list = []
    edge11_list = []

    wb = load_workbook(filename=path)
    sheets = wb.get_sheet_names()
    msg_all_tuple = []
    edge_all_list = []
    weight_list = [2.5, 2.0, 2.0, 2.0, 2.0, 2.5, 2.0, 3.0]
    for name in sheets:
        if "Shenzhen Metro Line " in name:
            i = name.strip("Shenzhen Metro Line ")
            ws = wb.get_sheet_by_name(name)
            rows = ws.rows
            locals()['line%s_tuple'%i] = []   #locals() 命名变量名
            locals()['line%s_list'%i] = []
            for row in rows:
                line = [col.value for col in row]
                station = line[0]
                sta_num = line[1]
                locals()['line%s_tuple'%i].append((station, sta_num))
                locals()['line%s_list'%i].append(sta_num)              
            msg_all_tuple.extend(locals()['line%s_tuple'%i])
            if int(i) >6:
                weight = weight_list[int((int(i)+3)/2)]
            else:
                weight = weight_list[int(i)-1]
            for k in range(len(locals()['line%s_list'%i])+1):
                try:
                    edge1 = (locals()['line%s_list'%i][k], locals()['line%s_list'%i][k+1])
                    locals()['edge%s_list'%i].append(edge1)
                    edge1_weight = (locals()['line%s_list'%i][k], locals()['line%s_list'%i][k+1], weight)
                    edge_all_list.append(edge1_weight)
                    if k != 0:
                        edge2 = (locals()['line%s_list'%i][k], locals()['line%s_list'%i][k-1])
                        edge2_weight = (locals()['line%s_list'%i][k], locals()['line%s_list'%i][k-1], weight)
                    else:
                        edge2 = (locals()['line%s_list'%i][-1], locals()['line%s_list'%i][-2])
                        edge2_weight = (locals()['line%s_list'%i][-1], locals()['line%s_list'%i][-2], weight)
                    locals()['edge%s_list'%i].append(edge2)
                    edge_all_list.append(edge2_weight)
                except:
                    pass
    return edge1_list,edge2_list,edge3_list,edge4_list,edge5_list,edge7_list,edge9_list,edge11_list,edge_all_list,msg_all_tuple

#建立网络，G
def BuildNetwok(edge_all_list):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edge_all_list)
    dict_key_edge = {}
    for i in edge_all_list:
        edge = (i[0], i[1])
        weight = i[2]
        dict_key_edge[edge] = weight
    return G, dict_key_edge
    
    
if __name__ == '__main__':
    file = r"F:\PA_learning_dataset\地铁.xlsx"
    start_time = time.clock()
    B = BestPath()
    edge1_list,edge2_list,edge3_list,edge4_list,edge5_list,edge7_list,edge9_list,edge11_list,edge_all_list,msg_all_tuple = ReadData(file)
    G, dict_all_edge = BuildNetwok(edge_all_list)
    list_all = msg_all_tuple
    edge = ('大新站','桃园站')
    target =  '八卦岭站'
    print('起始位置', edge[0], '-', '目的地', target)
    start = B.StartLocation(list_all, edge)
    target_re = B.NameReplace(list_all, target)
    result_edges = B.ShortedPathShow(list_all, G, dict_all_edge, start, target_re)
    print('转乘线路说明：')
    LineMoveOn(result_edges, edge1_list,edge2_list,edge3_list,edge4_list,edge5_list,edge7_list,edge9_list,edge11_list)
    list_result_node = []
    for r_edge in result_edges:
        if result_edges.index(r_edge) == 0:
            list_result_node.append(r_edge[0])
            list_result_node.append(r_edge[1])
        else:
            list_result_node.append(r_edge[1])
    list_all_op = NameEdge(list_all, list_result_node)
    print('地铁车站路径:')
    print(list_result_node,'\n', list_all_op)
    print('给网路设置布局...')
    fig = plt.figure(figsize=(20, 15), facecolor='white')
    pos = nx.spring_layout(G)
    print('画出网络图像：')
    nx.draw(G,pos,with_labels=True, edgelist = edge1_list, node_color='white', edge_color='g', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge2_list, node_color='white', edge_color='black', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge3_list, node_color='white', edge_color='y', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge4_list, node_color='white', edge_color='b', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge5_list, node_color='white', edge_color='0.9', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge7_list, node_color='white', edge_color='0.5', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge9_list, node_color='white', edge_color='0.8', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True, edgelist = edge11_list, node_color='white', edge_color='0.2', node_size=400, width=3, alpha=0.5, style='dashed')
    #    nx.draw(G,pos,with_labels=True, node_color='white', edge_color='b', node_size=400, width=3, alpha=0.5, style='dashed')
    nx.draw(G,pos,with_labels=True,nodelist = list_result_node, edgelist = result_edges, node_color='r', edge_color='r',width=3, node_size=500, alpha=0.5, style='dashed')
    plt.title('SZ Metro Network',fontsize=20)
    plt.show()
    end_time = time.clock()
    time = end_time - start_time
    print('time: %g s' %time)    

