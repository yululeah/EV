#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:48:24 2019
the instantaneous energy consumption rate was
 calculated as the product of real-time current and voltage.
 The relationship between the energy consumption factor and average travel speed.
@author: apple
"""

import numpy as np
import pandas as pd
import time
import os

datareinx_tab=pd.DataFrame([])

path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/hybrid16/'
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

#table_1=np.zeros((103,104))
time_start=time.time()
names=locals()


for i in range (1,len(file_list)):
    filename1='/Users/apple/Desktop/shakalaka/research_on_EV/data/ddatac/phev/ddatac'+str(i)+'.csv'
    filename2='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/phev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/shakalaka/research_on_EV/data/phev/ddatac'
#    filename1='D:/1/72282/ddata2c'+str(i)+'.csv'
#for i in range(300): 师姐
#    filename1='D:/1/72282/ddatac'+str(i)+'.csv'
#    filename2='D:1/72282/datareinx'+str(i)+'.csv'
#    path='D:/1/72282'  师姐
    if os.path.exists(filename1)==True:
        
        ddata=np.array(pd.read_csv(filename1))
        datareinx=pd.read_csv(filename2)

    datareinx_temp=datareinx[:]
    datareinx_temp['power']=datareinx_temp['current']*datareinx_temp['volt']/1000
    
    datareinx_temp=datareinx_temp[datareinx_temp['newspd']>0.5]
#    datareinx_temp=datareinx_temp[datareinx_temp['newspd']<70]
    datareinx_temp=datareinx_temp[datareinx_temp['power']>0.08]
#    datareinx_temp=datareinx_temp[datareinx_temp['power']<1]
    
    datareinx_tab=pd.concat([datareinx_tab,pd.DataFrame(datareinx_temp)],axis=0,ignore_index=True)

spd=np.array(datareinx_tab['newspd'])
power=np.array(datareinx_tab['power'])
spd_power=np.vstack((spd,power))
spd_power=np.transpose(spd_power) #转置

T=4
mid_temp=np.zeros((int(120/T),2))
for j in range(1,int(120/T)):
    temp=spd_power[spd_power[:,0]<j+T]
    temp=temp[temp[:,0]>j]
    if temp.shape[0]==0:
        mid_temp[j,0]=j
    else:
        temp=temp[temp[:,0]<j+T] #设置 速度 segment
        mid_temp[j,1]=np.mean(temp[:,1]) #分位数
#        mid_temp[j,1]=np.percentile(temp[:,1],50) #分位数
        mid_temp[j,0]=j*T
    
    