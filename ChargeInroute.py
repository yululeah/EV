# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 14:51:14 2018

@author: Administrator
"""

########chargeInRoute

import numpy as np
import pandas as pd
import getTimeDiff
from scipy import stats

def cin(ddata,datarinx):
    #ddata=ddata[ddata[:,4]!=0]
    lenr=-1
    rec=np.zeros((ddata.shape[0],10))
    lens=ddata.shape[0]
    i=0
    while i<lens-1:
        if ddata[i,1]==2:
            j=i+1
            #print(j)
            while j<lens-2:
                if ddata[j,1]==2 and (ddata[j,12]==100 or ddata[j,12]==30 or ddata[j,12]==123 or ddata[j,4]<0 or ddata[j,4]==0 or ddata[j,11])!=0 :
                    #i=j-1
                    #print(ddata[j,1])
                    #print(j+10000)
                    break 
                if ddata[j,1]==2 and ddata[j,12]!=100 and ddata[j,12]!=30 and ddata[j,12]!=123 and ddata[j,11]==0 and ddata[j,4]>0:
                    k=j+1
                    #print(k+100000)
                    
                    
                    while k<lens-2:
                        
                        if ddata[k,1]==2 :
                            #print(i,j,k)
                            lenr=lenr+1
                            rec[lenr,0]=ddata[i,2]##开始SOC
                            rec[lenr,1]=ddata[i,3]#
                            rec[lenr,2]=ddata[j,2]
                            rec[lenr,3]=ddata[j,3]
                            rec[lenr,4]=ddata[k,2]
                            rec[lenr,5]=ddata[j,4]##充电时长
                            rec[lenr,6]=getTimeDiff.GetTimeDiff(datarinx['time_collect'][ddata[j,2]],datarinx['time_collect'][ddata[j+1,2]])/60 #停留时长（下次行程开始-充电开始）
                            #print(datarinx['time_collect'][ddata[j+1,2]])
                            
                            rec[lenr,7]=ddata[j,6]#-ddata[j,5]
                            #print(i,j,k)
                            clevel=np.array(datarinx['current'][int(ddata[j,2]):int(ddata[j,3])])
                            #clevel=clevel[clevel<0]
                            
                            if len(clevel)<2:
                                rec[lenr,8]=10000
                            else:
                        
                                clevel=np.around(clevel,decimals=3)
                                #print(clevel)
                                rec[lenr,8]=stats.mode(clevel)[0][0]##current
                           
                            break
                            

                       
                        k=k+1
                    break

                j=j+1
        i=i+1
    #return rec


    #print(lenr)
    if lenr==-1:
        reg=np.zeros((1,11))
    if lenr!=-1:
        rec=rec[:lenr+1,:]

        reg=np.zeros((rec.shape[0],11))
        for j in range(reg.shape[0]):
            #print(j)
            reg[j,0]=datarinx['quqantity_electricity_percent'][int(rec[j,2])]  ##开始SOC
            reg[j,1]=datarinx['distance_accumulative'][rec[j,2]]-datarinx['distance_accumulative'][rec[j,1]]##上次行程距离
            reg[j,2]=datarinx['distance_accumulative'][rec[j,4]]-datarinx['distance_accumulative'][rec[j,3]]###下次行程距离
            reg[j,3]=rec[j,5] ##充电时长
            reg[j,4]=rec[j,6] ##停留时长
            reg[j,5]=rec[j,7]##充电电量
            reg[j,6]=rec[j,8]#充电功率current
            reg[j,7]=pd.Timestamp(datarinx['time_collect'][rec[j,2]]).weekday()#工作日标记
            reg[j,8]=pd.Timestamp(datarinx['time_collect'][rec[j,2]]).hour+pd.Timestamp(datarinx['time_collect'][rec[j,2]]).minute/60##充电时间
            reg[j,9]=(datarinx['quqantity_electricity'][rec[j,1]]-datarinx['quqantity_electricity'][rec[j,2]])/reg[j,1]##上段行程能耗
            reg[j,10]=datarinx['quqantity_electricity'][int(rec[j,3])]-datarinx['quqantity_electricity'][int(rec[j,2])]
            
    return reg




                    