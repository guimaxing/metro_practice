# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:44:40 2018
@author: Moc
"""
import networkx as nx
#from ForRoadMap import BestPath, NameEdge, LineMoveOn
import operator

"""
首先是道路的拥堵预测判断
前往目的地的路线拥堵程度判断
当超过某个指标认为该路段拥堵严重
返回最拥堵的路口进行管控
"""
#拥堵预测
def Congestion(time, standard_time):
    if time >standard_time:
        return '拥堵'
    else:
        return '畅通'
       
        
#道路判断
def RoadJuidge(juidge_line):   #line 的形式为[roadline, time]
    time = juidge_line[1]
    standard_time = input()   #输入纯数字
    result = Congestion(time, standard_time)
    if result == '畅通':
        pass
    else:
        dict_speed = {}
        for node in juidge_line:
            acttime = SpeedActualTime(node)
            nortime = SpeedNormal(node)
            D_value = nortime - acttime
            dict_speed[node] = D_value
        dict_speed_new = sorted(dict_speed.items(),key = operator.itemgetter(1))
        list_speed_new = list(dict_speed_new.keys())
        return list_speed_new[-1]  #返回路线中最拥堵的卡口
        
"""
节点的拥堵预测判断
通过某个指标判断，认为该卡口严重拥堵
返回该拥堵卡口的最优疏散邻居卡口
"""

#加入通过节点的速度，拥堵指标判断
def SpeedNormal(node):   #正常卡口通过速度
    speed_normal_dict = {'node':'speed'}
    speed_normal = speed_normal_dict[node]
    return speed_normal

def SpeedActualTime(node):   #实时卡口通过速度
    speed_actual_dict = {'node':'speed'}
    speed_actual = speed_actual_dict[node]
    return speed_actual
   
#卡口的邻居节点列表
def GetNeighbor(G, node):
    list_nei = nx.neighbors(G, node)
    return list_nei


#遣返或者引导疏散路线
def Evacuated(target, node):
    D_value = SpeedNormal(target) - SpeedActualTime(target)
    if D_value/SpeedActualTime(target) > 2: #小于正常速度的3倍, 表明目的地拥堵严重， 遣返
        return 'go back'
    else:
        list_nei = GetNeighbor(node)
        dict_nei = {}
        for item in list_nei:
            D_value_node = SpeedNormal(node) - SpeedActualTime(node)   #判断此时该卡口的邻居节点拥堵情况，列出最不拥堵的卡口，疏散
            dict_nei[item] = D_value_node
        dict_nei_new = sorted(dict_nei.items(),key = operator.itemgetter(1))
        list_nei_new = list(dict_nei_new.keys())
        return list_nei_new[0]  #推荐最优卡口











