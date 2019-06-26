#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:10:42 2019
纯电模式
@author: apple
"""

import os
import time
import numpy as np
import pandas as pd
import getTimeDiff
import calorific_value
import datetime

path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/hybrid16/'
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)


T=8 #5min
timestart=time.time()


size=9
data_divert_T=np.zeros((1,size))

for i in range (1,len(file_list)):
    filename='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/phev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/shakalaka/research_on_EV/data/phev/ddatac'
    filename2='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/phev的副本/datareinx'+str(i)+'.csv'
   
    if os.path.exists(filename)==True:
        datareinx=pd.read_csv(filename)
        datareinx_temp=pd.read_csv(filename2)  #取timecollect的秒数
        ahd=datareinx_temp.pop('time_collect')
        datareinx.insert(0,'time_collect2',ahd)
        
#        #为了获取加速度
#        #构造一列速度差；一列时间差
        datareinx['time_diff']=0.0000000000001
        datareinx['speed_diff']=0
        datareinx['acc']=0
        
        datareinx['time_diff'].loc[0:len(datareinx)-2]=(np.array(datareinx['time_collect2'].loc[1:len(datareinx)-1])-np.array(datareinx['time_collect2'].loc[0:len(datareinx)-2]))*24*60*60
        datareinx['speed_diff'].loc[0:len(datareinx)-2]=(np.array(datareinx['speed'].loc[1:len(datareinx)-1])-np.array(datareinx['speed'].loc[0:len(datareinx)-2]))
        datareinx['acc']= datareinx['speed_diff']/3.6/datareinx['time_diff']
        #先取出所有行驶状态
        datareinx_driving=datareinx[datareinx['statusn2']==1]
#        datareinx2=datareinx_driving[datareinx_driving['fuel_consumption']>500]
        datareinx3=datareinx_driving[datareinx_driving['fuel_consumption']<300]
        
        
        #找到soc在下降且瞬时液体燃料消耗量不为0的取出来
        datareinx3 = datareinx3.reset_index(drop=True)
        

     
        index=np.array(datareinx3['index'].loc[1:len(datareinx3)-1])-np.array(datareinx3['index'].loc[0:len(datareinx3)-2])
        stop=np.transpose(np.array(np.where(index>1))) #找到行程的结尾
        start=stop+1
        start=np.unique(np.vstack((np.array([0]),start)))
        stop=np.unique(np.vstack((stop,np.array([len(datareinx3)-1]))))
        
        qe=datareinx['quqantity_electricity']
        qep=datareinx['quqantity_electricity_percent']
        da=datareinx['distance_accumulative']
        fc=datareinx['fuel_consumption']
        tc=datareinx['time_collect']
        ac=datareinx['acc']
        
        for j in range (0,len(start)-1):
            a=datareinx['index'].loc[start[j]] #索引
            b=datareinx['index'].loc[stop[j]]  #索引
            
            data_olas=np.zeros((1,5))
                    
            fcc=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
            fce=qep.loc[a]-qep.loc[b] #soc
            vmt=da.loc[b]-da.loc[a] #距离
            tcc=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b]) # 时间
            
            daa=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
            dau=da.loc[a:b-1].reset_index(drop=True) 
            fcb=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
            fca=sum((daa-dau)*fcb/100) # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量
            
    # =============================================================================
                     
    
            k=a
            #                for k in range((index_start,index_end)):
            while k<b:
                time_start=datareinx['time_collect'].loc[k]
                da_start=datareinx['distance_accumulative'].loc[k]
                qe_start=datareinx['quqantity_electricity'].loc[k]
                qep_start=datareinx['quqantity_electricity_percent'].loc[k]
    #                fa_start=datareinx_temp['fuel_accumulate'].loc[k]
                a=k
                
                while getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k])<T*60 and k<b :#如果在5分钟内
                    k=k+1
            #break出来的时候，就是找到了那个大于5分钟的值？
            
                daaa=da.loc[a+1:k-1].reset_index(drop=True) #distance_accumulative
                dauu=da.loc[a:k-2].reset_index(drop=True) 
                fcbb=fc.loc[a+1:k-1].reset_index(drop=True) #fuel_consumption
            #持续时间、路程、电能变化，soc、燃油变化,星期，小时,温度，加速度
                data_divert_T_temp=np.hstack((getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k-1]), \
                                          datareinx['distance_accumulative'].loc[k-1]-da_start, \
                                          qe_start-datareinx['quqantity_electricity'].loc[k-1], \
                                          (qep_start+datareinx['quqantity_electricity_percent'].loc[k-1])/2, \
                                          sum((daaa-dauu)*fcbb/100000*8.9), \
                                          datetime.datetime.strptime(datareinx['time_collect'].loc[k-1],"%Y-%m-%d %H:%M:%S").weekday()+1, \
                                          datetime.datetime.strptime(datareinx['time_collect'].loc[k-1],"%Y-%m-%d %H:%M:%S").hour, \
                                          datareinx['high_temperature'].loc[k-1], \
                                          np.mean(datareinx['acc'].loc[a:k-1])))   
                
                data_divert_T=np.vstack((data_divert_T,data_divert_T_temp))
            

                
    # =============================================================================



    
    
    
    print(i)
    print(time.time()-timestart) 
    
    
# =============================================================================   
#数据处理
#删去路程为0的
data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,1]<0.0000001),axis=0)
#8分钟 最多跑16km
data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,1]>16),axis=0)
#    温度小于0的删
data_divert_T=data_divert_T[data_divert_T[:,7]>0]

data_divert_T = np.hstack((data_divert_T,np.zeros((len(data_divert_T),6))))
#构造速度和ecr
data_divert_T[:,size]=data_divert_T[:,1]/data_divert_T[:,0]*3600  #构造速度
data_divert_T[:,size+1]=(data_divert_T[:,2]+data_divert_T[:,4])/data_divert_T[:,1]#构造ecr
data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,size+1]<=0),axis=0)
#    data_divert_T[:,size+2]=data_divert_T[:,4]/data_divert_T[:,2]#ratio

#是否highway
data_divert_T[np.where(data_divert_T[:,7]>=65),size+3]=1 #是
data_divert_T[np.where(data_divert_T[:,7]<65),size+3]=0 #不是
#是否工作日
data_divert_T[np.where(data_divert_T[:,5]<6),size+4]=1 #是
data_divert_T[np.where(data_divert_T[:,5]>5),size+4]=0 #不是
#是否高峰
data_divert_T[np.where(data_divert_T[:,6]==7),size+5]=1 #是
data_divert_T[np.where(data_divert_T[:,6]==8),size+5]=1 #是
data_divert_T[np.where(data_divert_T[:,6]==9),size+5]=1 #是
data_divert_T[np.where(data_divert_T[:,6]==17),size+5]=1 #是
data_divert_T[np.where(data_divert_T[:,6]==18),size+5]=1 #是
data_divert_T[np.where(data_divert_T[:,6]==16),size+5]=1 #是
    
# =============================================================================
    
np.mean(data_divert_T[:,size+1])
import matplotlib.pyplot as plt
plt.hist(data_divert_T[:,size+1], 20, normed=True)   #####bins=30