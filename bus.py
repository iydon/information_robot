# -*- coding: utf-8 -*-
# 巴士时间
from time import localtime, asctime

def routine():
    xyday = [[7,20],[7,23],[7,23],[7,26],[7,29],[7,29],[7,32],[7,35],[7,35],[7,38],[7,41],[7,41],[7,45],[7,45],(7,50),(7,55),(8,0),(8,5),(8,10),(8,15),(8,20),(8,25),(8,30),(8,35),(8,40),(8,45),(8,50),(8,55),(9,0),(9,15),(9,30),[9,45],(9,50),[9,53],[9,56],(10,0),[10,3],[10,6],[10,9],(10,10),(10,15),(10,20),(10,30),(10,40),(10,50),(11,0),(11,15),(11,30),(11,45),(12,0),[12,5],(12,10),[12,15],[12,18],(12,21),[12,24],[12,27],(12,30),[12,33],[12,36],(12,40),(12,50),(13,0),(13,10),(13,20),[13,23],[13,26],(13,29),[13,32],[13,35],(13,38),[13,40],(13,40),(13,50),(14,0),(14,15),(14,30),(14,45),(15,0),(15,15),(15,30),(15,45),(15,50),[15,53],[15,56],(15,56),[15,59],[16,2],(16,2),[16,5],[16,5],(16,10),(16,15),(16,30),(16,45),(17,0),(17,15),(17,30),(17,45),(18,0),(18,10),[18,13],[18,16],(18,19),[18,22],[18,25],(18,28),(18,30),(18,35),(18,40),(18,45),(18,50),(18,55),(19,0),(19,5),(19,10),(19,15),(19,20),(19,25),(19,30),(19,45),(20,0),(20,15),(20,30),(20,45),(21,0)]
    kyday = [[7,30],[7,33],[7,36],(7,40),[7,43],[7,47],(7,51),(7,55),(8,0),(8,10),(8,15),(8,20),(8,25),(8,30),(8,35),(8,40),(8,45),(8,50),(8,55),(9,0),(9,10),(9,15),(9,20),(9,30),(9,40),(9,50),[9,55],(10,0),[10,3],(10,5),[10,10],(10,10),(10,15),(10,20),(10,25),(10,30),(10,35),(10,40),(10,50),(11,0),(11,15),(11,30),(11,45),(12,0),(12,10),(12,20),[12,23],[12,26],(12,29),[12,32],[12,35],(12,38),[12,41],(12,50),(13,0),(13,15),(13,30),[13,33],[13,36],(13,39),[13,42],[13,45],(13,50),(14,0),(14,15),(14,30),(14,40),(14,50),(15,0),(15,10),(15,20),(15,30),(15,40),(15,50),[15,53],[15,56],[15,59],(16,2),[16,5],[16,8],(16,11),[16,14],[16,17],(16,20),(16,30),(16,40),(16,50),(17,0),(17,10),(17,20),(17,30),(17,40),(17,50),(18,0),[18,5],(18,10),(18,15),[18,18],[18,21],(18,24),[18,27],(18,30),(18,45),(19,0),(19,15),(19,30),(19,45),(20,0),(20,15),(20,30),(20,45),(21,0),[21,5],(21,10),[21,15],(21,20),[21,25],(21,30),(21,45),(22,0),(22,0)]
    xyend = [(7,30),(8,0),(8,30),(9,0),(9,30),(10,0),(10,30),(11,0),(11,30),(12,0),(12,30),(13,0),(13,30),(14,0),(14,30),(15,0),(15,30),(16,0),(16,30),(17,0),(17,30),(18,0),(18,30),(19,0),(20,0),(21,0),(21,40)]
    kyend = [(7,50),(8,20),(8,50),(9,20),(9,50),(10,20),(10,50),(11,20),(11,50),(12,20),(12,50),(13,20),(13,50),(14,20),(14,50),(15,20),(15,50),(16,20),(16,50),(17,20),(17,50),(18,20),(19,20),(20,20),(21,20),(22,0),(22,10)]
    return {'xyday':xyday, 'kyday':kyday, 'xyend':xyend, 'kyend':kyend}

def bustimereturn(s, bias=0):
    cur_time = localtime()
    cur_hour,cur_min = cur_time[3],cur_time[4]
    dct      = routine()
    getIdx   = lambda k: [i<(60*cur_hour+cur_min) for i in [60*h+m for h,m in dct[k]]].index(False)-bias
    res = '%s\n'%asctime()
    try:
        idx = getIdx('xy%s'%s)
        if isinstance(dct['xy%s'%s][idx], list):
            res += "高峰线: "
        res += '欣园：%02d:%02d\n'%(dct['xy%s'%s][idx][0],dct['xy%s'%s][idx][1])
    except:
        res += '欣园已无车\n'
    try:
        idx = getIdx('ky%s'%s)
        if isinstance(dct['ky%s'%s][idx], list):
            res += "高峰线: "
        res += '科研楼：%02d:%02d'%(dct['ky%s'%s][idx][0],dct['ky%s'%s][idx][1])
    except:
        res += '科研楼已无车'
    return res

def bustime(option=None):
    cur_wday = localtime()[6] if option==None else int(option)
    return "\n\n".join([(bustimereturn('day',-i) if cur_wday in [0, 1, 2, 3, 4] else (bustimereturn('end',-i) if cur_wday in [5, 6] else '404')) for i in range(2)])
    # if cur_time_wday in [0, 1, 2, 3, 4]:
    #     return bustimereturn('day')
    # elif cur_wday in [5, 6]:
    #     return bustimereturn('end')
    # else:
    #     return '404'

print(bustime())