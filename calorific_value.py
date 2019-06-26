#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:39:03 2019

@author: apple
探究每个行程
探究单位里程热值与不同速度区间的关系。
"""
import numpy as np
import pandas as pd
import getTimeDiff


#处理每个行程
#filename='tab2.csv'
#data=pd.read_csv(filename)

def calorific_value(data,p):
    ##添两列空白的
    data = np.hstack((data,np.zeros((len(data),2))))
    
    T=5   #设置时间间隔
    c=np.zeros((int(100/T),1))  ##速度与热值
    d=np.zeros((int(100/T),1))  ##soc与热值
    data[:,6]=data[:,2]/data[:,4]  #构造速度
#    #油电混用
    data[:,7]=(data[:,0]+data[:,1]/1000*p)/data[:,2]#构造每km总热值
#    #只用油
#    data[:,7]=data[:,1]/data[:,2]
    #只用电
#    data[:,7]=data[:,0]/data[:,2]
    
    for i in range(1,int(100/T)):
        #速度
        data_temp1=data[data[:,6]>i*T]
        data_temp1=data_temp1[data_temp1[:,6]<=(i+1)*T]
        c[i,0]=np.mean(data_temp1[:,7])
        ##或者平均数？？
        
         ##soc的影响
        data_temp2=data[data[:,5]>i*T]
        data_temp2=data_temp2[data_temp2[:,5]<=(i+1)*T]
#        data_temp2=data.loc[data['soc']>i*10]
#        data_temp2=data_temp2.loc[data_temp2['soc']<=(i+1)*10]
        d[i,0]=np.mean(data_temp2[:,7])
        
    return c,d

def calorific_value2(data,p):
    ##添两列空白的
    data = np.hstack((data,np.zeros((len(data),2))))
    
    data[:,5]=data[:,1]/data[:,0]*3600  #构造速度
    data[:,6]=(data[:,2]+data[:,4]/1000*p)/data[:,1]#构造每km总热值

    data=np.delete(data,np.where(data[:,6]<0),axis=0)  #删热值小于0的
    
        
    return data

def calorific_value3(data):
    
    T=5   #设置时间间隔
    c=np.zeros((int(100/T),int(100/T)))  ##速度\soc与热值

    
    for i in range(1,int(100/T)):
        for j in range(1,int(100/T)):
            data_temp1=data[data[:,5]>i*T]  #速度
            data_temp1=data_temp1[data_temp1[:,5]<=(i+1)*T]
            data_temp1=data_temp1[data_temp1[:,3]>j*T]  #soc
            data_temp1=data_temp1[data_temp1[:,3]<=(j+1)*T]
            c[i-1,j-1]=np.mean(data_temp1[:,6])
        
    return c
#####################################处理每5分钟
#filename='tabb.csv'
#data=pd.read_csv(filename)

def calorific_value_Tmin(data_divert_tab):
#    data_divert_tab = np.hstack((data_divert_tab,np.zeros((len(data_divert_tab),2))))
    T=5   #设置速度、soc间隔
    c=np.zeros((int(100/T),1))  ##速度与热值
    d=np.zeros((int(100/T),1))  ##soc与热值
#    data_divert_tab[:,5]=data_divert_tab[:,1]/data_divert_tab[:,0]*3600  #构造速度
#    data_divert_tab[:,6]=(data_divert_tab[:,2]+data_divert_tab[:,4])/data_divert_tab[:,1]#构造每km总热值
    
#    data_divert_tab=np.delete(data_divert_tab,np.where(data_divert_tab[:,6]>6),axis=0)
    
    for i in range(1,int(100/T)):
        
        data_temp1=data_divert_tab[data_divert_tab[:,9]>(i-1)*T]
        data_temp1=data_temp1[data_temp1[:,9]<=i*T]
#        data_temp1=data.loc[data['speed']>i*T]
#        data_temp1=data_temp1.loc[data_temp1['speed']<=(i+1)*T]
        c[i-1,0]=np.mean(data_temp1[:,10])
        ##或者平均数？？
        
        ##soc的影响
        data_temp2=data_divert_tab[data_divert_tab[:,3]>(i-1)*T]
        data_temp2=data_temp2[data_temp2[:,3]<=i*T]
#        data_temp2=data.loc[data['soc']>i*10]
#        data_temp2=data_temp2.loc[data_temp2['soc']<=(i+1)*10]
        d[i-1,0]=np.mean(data_temp2[:,10])
        
    return c,d

#datareinx_drive=datareinx[datareinx['statusn2']==1].reset_index(drop=True)
#data_tab=np.zeros((len(datareinx_drive),5))
#
#
#for j in range(len(datareinx_drive)-1):
#    
#    if getTimeDiff.GetTimeDiff(datareinx_drive['time_collect'].loc[j],datareinx_drive['time_collect'].loc[j+1])<1.5*60 :
#        data_tab[j,0]=datareinx_drive['quqantity_electricity_percent'].loc[j]  #soc
#        data_tab[j,1]=datareinx_drive['newspd'].loc[j+1]  #v
#        data_tab[j,2]=(datareinx_drive['newspd'].loc[j+1]-datareinx_drive['newspd'].loc[j])/ getTimeDiff.GetTimeDiff(datareinx_drive['time_collect'].loc[j],datareinx_drive['time_collect'].loc[j+1])  #a
#        data_tab[j,3]=datareinx_drive['quqantity_electricity'].loc[j]-datareinx_drive['quqantity_electricity'].loc[j+1]  #电能
#        data_tab[j,4]=(datareinx_drive['distance_accumulative'].loc[j+1]-datareinx_drive['distance_accumulative'].loc[j])*datareinx_drive['fuel_consumption'].loc[j]  #fuel
