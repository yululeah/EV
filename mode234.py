#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 18:34:30 2019

@author: apple
"""
import os
import time
import numpy as np
import pandas as pd
import getTimeDiff
import calorific_value
import datetime


    
def unique_index(L,f):
    """L表示列表， i表示索引值，v表示values，f表示要查找的元素 """
    return [i for (i,v) in enumerate(L) if v==f]   




path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/hybrid16/'
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

T=4 #8min
timestart=time.time()


size=10
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
        datareinx2=datareinx_driving[datareinx_driving['fuel_consumption']>500]
        datareinx3=datareinx_driving[datareinx_driving['fuel_consumption']<300]
        
        
        #找到soc在下降且瞬时液体燃料消耗量不为0的取出来
        datareinx2 = datareinx2.reset_index(drop=True)
        

     
        index=np.array(datareinx2['index'].loc[1:len(datareinx2)-1])-np.array(datareinx2['index'].loc[0:len(datareinx2)-2])
        stop=np.transpose(np.array(np.where(index>1))) #找到行程的结尾
        start=stop+1
        start=np.unique(np.vstack((np.array([0]),start)))
        stop=np.unique(np.vstack((stop,np.array([len(datareinx2)-1]))))
        
        qe=datareinx['quqantity_electricity']
        qep=datareinx['quqantity_electricity_percent']
        da=datareinx['distance_accumulative']
        fc=datareinx['fuel_consumption']
        tc=datareinx['time_collect']
        ac=datareinx['acc']
        speed=datareinx['speed']
        
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
                
                #找到启动阶段/运行阶段
                count_all=k-a  #有多少个数据
                count_0=list(speed.loc[a:k-1]).count(0)  #有多少个0
                count_positive=count_all-count_0  #有多少个大于0
                if count_0!=0:
                    index_0=unique_index(list(speed.loc[a:k-1]),0)  #找到所有速度为0的坐标
                    index_po = [i+1+a for i in index_0] #找到所有速度为0的坐标+1
                    count_po=count_0-list(speed.loc[index_po]).count(0)##找到这些数，数有多少大于个0，那就有多少组启动
                else:
                    count_po=0#都在运行阶段
                ratio_start_up=count_po*2/count_all
                    
                
            #持续时间、路程、电能变化，soc、燃油变化,星期，小时,温度，加速度
                data_divert_T_temp=np.hstack((getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k-1]), \
                                          datareinx['distance_accumulative'].loc[k-1]-da_start, \
                                          qe_start-datareinx['quqantity_electricity'].loc[k-1], \
                                          (qep_start+datareinx['quqantity_electricity_percent'].loc[k-1])/2, \
                                          sum((daaa-dauu)*fcbb/100000*8.9), \
                                          datetime.datetime.strptime(datareinx['time_collect'].loc[k-1],"%Y-%m-%d %H:%M:%S").weekday()+1, \
                                          datetime.datetime.strptime(datareinx['time_collect'].loc[k-1],"%Y-%m-%d %H:%M:%S").hour, \
                                          datareinx['high_temperature'].loc[k-1], \
                                          np.mean(datareinx['acc'].loc[a:k-1]), \
                                          ratio_start_up))   
                
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
data_divert_T[np.where(data_divert_T[:,size]>=65),size+3]=1 #是
data_divert_T[np.where(data_divert_T[:,size]<65),size+3]=0 #不是
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
#   提取行车充电的
data_divert_charging=data_divert_T[np.where(data_divert_T[:,2]<0)]
# =============================================================================
#   提取燃油模式的
data_divert_ICE=data_divert_T[np.where(data_divert_T[:,2]==0)]
data_divert_ICE=data_divert_ICE[np.where(data_divert_ICE[:,4]>=0.0000001)]
# =============================================================================
#   提取混合驱动模式
#删去充电的，没有用油的
data_divert_hybrid=data_divert_T
data_divert_hybrid=np.delete(data_divert_hybrid,np.where(data_divert_hybrid[:,2]<0.0000001),axis=0)
data_divert_hybrid=np.delete(data_divert_hybrid,np.where(data_divert_hybrid[:,4]<0.0000001),axis=0)

#删去1分钟内的行程
data_divert_hybrid=np.delete(data_divert_hybrid,np.where(data_divert_hybrid[:,0]<63),axis=0)
#8分钟 最多烧12kwh油
data_divert_hybrid=np.delete(data_divert_hybrid,np.where(data_divert_hybrid[:,4]>1.5*T),axis=0)
data_divert_hybrid=data_divert_hybrid[data_divert_hybrid[:,size+1]<2]
    
# =============================================================================

    
def process(data_divert_T):
    
    day_rezhi=np.zeros((24,1))
    for k in range(0,23):
        temp=data_divert_hybrid[data_divert_hybrid[:,6]==k] #24小时
        temp=temp[temp[:,5]<6] #时间
        day_rezhi[k,0]=np.median(temp[:,size+1])
    
    #startup
    binbin=5
    startup=np.zeros((20,1))
    for k in range(1,20):
        temp=data_divert_hybrid[data_divert_hybrid[:,size]>k*binbin] #24小时
        temp=temp[temp[:,size]<=(k+1)*binbin] #时间
        startup[k,0]=np.mean(temp[:,9])  #平均start——up
        
    #温度
    tem=np.zeros((33,1))
    for k in range(21,54):
        temp=data_divert_hybrid[data_divert_hybrid[:,7]==k] 
        tem[k-21,0]=np.mean(temp[:,size+1])
    
    #acce
    acce=np.zeros((24,1))
    for k in range(-12,12):
        temp=data_divert_hybrid[data_divert_hybrid[:,8]>k/100] 
        temp=temp[temp[:,8]<(k+1)/100] 
        acce[k+12,0]=np.mean(temp[:,size+1]) 
    #vv
    vv=np.zeros((20,1))  ##速度与热值
    for k in range(1,20):
        data_temp1=data_divert_hybrid[data_divert_hybrid[:,size]>(k-1)*5]
        data_temp1=data_temp1[data_temp1[:,size]<=k*5]
#        data_temp1=data.loc[data['speed']>i*T]
#        data_temp1=data_temp1.loc[data_temp1['speed']<=(i+1)*T]
        vv[k-1,0]=np.mean(data_temp1[:,size+1])    
    
     ##soc的影响
     socc=np.zeros((20,1))  ##速度与热值
     for k in range(1,20):
        data_temp2=data_divert_hybrid[data_divert_hybrid[:,3]>(k-1)*5]
        data_temp2=data_temp2[data_temp2[:,3]<=k*5]
#        data_temp2=data.loc[data['soc']>i*10]
#        data_temp2=data_temp2.loc[data_temp2['soc']<=(i+1)*10]
        socc[k-1,0]=np.median(data_temp2[:,size+1])
        
    #v&acce
    binbin=5
    binbin2=2
    v_acce=np.zeros((20,12))  ##v\acce与ecr
    for i in range(1,20):
        for j in range(-6,6):
            data_temp1=data_divert_hybrid[data_divert_hybrid[:,size]>i*binbin]  #速度
            data_temp1=data_temp1[data_temp1[:,size]<=(i+1)*binbin]
            data_temp1=data_temp1[data_temp1[:,8]>j*binbin2/100]  #acce 
            data_temp1=data_temp1[data_temp1[:,8]<=(j+1)*binbin2/100]
            v_acce[i-1,j+6]=np.mean(data_temp1[:,size+1])
            
            
    #trip dis
    diss=np.zeros((16,1))
    for k in range(1,16):
        temp=data_divert_hybrid[data_divert_hybrid[:,1]==k] 
        diss[k,0]=np.mean(temp[:,size+1]) 
    #分析相关性
    cor=np.corrcoef(data_divert_T2,rowvar=0)

    return day_rezhi,tem,acce
    
    

    