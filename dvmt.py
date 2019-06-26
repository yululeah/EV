# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 04:42:59 2018

@author: Administrator
"""
import numpy as np
import pandas as pd


def dvmt1(datareinx):   #  daily vehicle miles traveled 
#    import getTimeDiff
    timec=datareinx['time_collect']
    timecp=pd.to_datetime(timec)
    ododvm=[]
    i=1
    while i<len(datareinx)-1:
        a2=timecp[i-1].day
        a1=timecp[i].day
        odom=datareinx['distance_accumulative']
        odom1=odom[i]
        if a1!=a2:
            j=i+1
            while timecp[j].day==a1 and j<len(datareinx)-1:
                j=j+1
                if j > len(datareinx)-2:
                    break
            
            ododvm.append(odom[j-1]-odom[i])
            #print(odom[j-1]-odom[i],a1)
            i=j
        i=i+1
    ododvm=np.array(ododvm)
    ododvm=ododvm[ododvm>=0]
    #ododvm=ododvm[ododvm<500]
    min1=min(ododvm)
    f25=np.percentile(ododvm,25)
    medi=np.median(ododvm)
    f27=np.percentile(ododvm,75)
    max1=max(ododvm)
    m1=np.mean(ododvm)
    m2=np.mean(ododvm[ododvm>0])
    
    return min1,f25,medi,f27,max1,m1,m2,ododvm
###最小值 20分位数 50分位数 75分位数 最大值，平均值，除小于0之后的平均值，

def commutea(ddata,datareinx):
    comdis=[]
    odom=datareinx['distance_accumulative']
    i=0
    while i <ddata.shape[0]-1:
       
        if ddata[i,12]==100 and ddata[i,13]==30:
            d=ddata[i,11]
            comdis.append(d)
        if ddata[i,12]==30 and ddata[i,13]==100:
            d=ddata[i,11]
            comdis.append(d)   
        
        if ddata[i,12]==100 and ddata[i,13]!=30:
            j=i+1
            while (ddata[j,0]==ddata[i,0]) and j<ddata.shape[0]-1:
                if ddata[j,13]==30:
                    d=odom[ddata[j,3]]-odom[ddata[i,2]]
                    comdis.append(d)
                    #print(i,j)
                    break
            
                j=j+1
            
        if ddata[i,12]==30 and ddata[i,13]!=100:
            j=i+1
            while (ddata[j,0]==ddata[i,0]) and j< ddata.shape[0]-1:
                if ddata[j,13]==100:
                    d=odom[ddata[j,3]]-odom[ddata[i,2]]
                    comdis.append(d)
                    
                    break
            
                j=j+1
        
        i=i+1
    comdis=np.array(comdis)
    cs=np.mean(comdis[comdis>0])
    return cs