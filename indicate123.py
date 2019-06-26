# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 20:21:28 2018

@author: anita
"""


import latlon
import numpy as np

def indichwp(ddata,work_place,home_place):

#ddata=ddata[(ddata[:,-1]+ddata[:,1]=0]
    ag=np.zeros((ddata.shape[0],ddata.shape[1]+2))
    ag[:,0:-2]=ddata
##要保证家和工作地的地点不一样
    if latlon.haversine(work_place.iloc[0],work_place.iloc[1],home_place.iloc[0],home_place.iloc[1])<2000:
####表明此时工作地和家的距离过于接近
        for i in range(ddata.shape[0]):
            if latlon.haversine(home_place.iloc[0],home_place.iloc[1],ddata[i,7],ddata[i,8])<2000:
                ag[i,-2]=123
            if latlon.haversine(home_place.iloc[0],home_place.iloc[1],ddata[i,9],ddata[i,10])<2000:
                ag[i,-1]=123
    
    
    else:
        for i in range(ddata.shape[0]):
            if latlon.haversine(work_place.iloc[0],work_place.iloc[1],ddata[i,7],ddata[i,8])<2000:
                ag[i,-2]=30
            if latlon.haversine(work_place.iloc[0],work_place.iloc[1],ddata[i,9],ddata[i,10])<2000:
                ag[i,-1]=30
            if latlon.haversine(home_place.iloc[0],home_place.iloc[1],ddata[i,7],ddata[i,8])<2000:
                ag[i,-2]=100
            if latlon.haversine(home_place.iloc[0],home_place.iloc[1],ddata[i,9],ddata[i,10])<2000:
                ag[i,-1]=100
    return ag
