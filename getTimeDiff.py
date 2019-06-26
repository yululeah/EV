# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 21:28:18 2018

@author: XPS
"""


def GetTimeDiff(timeStra,timeStrb):
    import time
    import datetime
    if timeStra>=timeStrb:
        return 0
    ta=time.strptime(timeStra,"%Y-%m-%d %H:%M:%S")
    tb=time.strptime(timeStrb,"%Y-%m-%d %H:%M:%S")
#    secondsDiff=time.mktime(time.strptime(timeStrb,"%Y-%m-%d %H:%M:%S"))-time.mktime(time.strptime(timeStra,"%Y-%m-%d %H:%M:%S"))
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)
    secondsDiff=(dataTimeb-dataTimea).total_seconds()
    return secondsDiff