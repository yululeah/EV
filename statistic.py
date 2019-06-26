#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 14:20:00 2019

@author: yulu
"""
"""
1、用户出行特征：
    1、1次均出行特征：
        BEV、PHEV工作日次均行驶里程分布；BEV、PHEV周末次均行驶里程分布
        BEV、PHEV工作日次均行驶时长；BEV、PHEV周末次均行驶时长
    1、2日均出行特征：
        BEV、PHEV工作日日均行驶里程分布；BEV、PHEV周末日均行驶里程分布
        BEV、PHEV工作日日均出行次数；BEV、PHEV周末日均出行次数
        BEV、PHEV工作日日均行驶时长；BEV、PHEV周末日均行驶时长
        BEV、PHEV工作日车辆出行时刻的具体分布数据，BEV、PHEV周末车辆出行时刻的分布直接结论，
        概述BEV、PHEV在工作日和周末的出行特征变化。
        行程开始、结束soc特征
        早晚高峰车速特征（分工作日和周末）行程开始结束都在am7-9；pm5-7
        出行od热力图？

2、用户充电特征：
    日充电频率；周充电频率；
    充电时刻与出行时刻分布对比、次均充电时长特征分析；
    单次充电时长
    充电开始、结束soc；
    每次充入的soc；
    充电地点热力图？
"""
import numpy as np
import consumptionana

def stat(ddata,datareinx):
#    date=ddata[:,0]#0:第几天；
#    statues=ddata[:,1]#1:状态：充电2；行驶1
#    #2:开始索引
#    #3:结束索引
#    during=ddata[:,4]#4:持续时间
#    soc_start=ddata[:,5]#5:开始soc
#    soc_end=ddata[:,6]#6:结束soc
#    #7：开始经度
#    #8：开始纬度
#    #9：结束经度
#    #10：结束纬度
#    distance=ddata[:,11]#11：距离
#    weekday=ddata[:,12]#12：星期几


####用户出行特征
    ddata_driving=ddata[ddata[:,1]==1]
    stat_driving_period=np.zeros((ddata_driving.shape[0],11))  #每次
    stat_driving_day=np.zeros((np.unique(ddata_driving[:,0]).shape[0],5))  #每天
    
    
##次均
    stat_driving_period[:,0]=ddata_driving[:,0]#0:第几天；
#分工作日/周末，第一栏为其索引，0:工作日；1：周末
    for j in range(ddata_driving.shape[0]):
        if ddata_driving[j,12]>5:
             stat_driving_period[j,1]=1 #周末
        else:
             stat_driving_period[j,1]=0 #工作日
        #次均行驶里程分布✨✨✨✨
        stat_driving_period[j,2]=ddata_driving[j,11]
        #次均行驶时长✨✨✨✨
        stat_driving_period[j,3]=ddata_driving[j,4]/60
        #第几天
        #stat_driving_period[j,4]=ddata_driving[j,0]
        
        #是否高峰（早高峰1晚高峰2平峰0）行程开始结束都在am7-9；pm5-7
        if  ddata_driving[j,13]>7 and ddata_driving[j,14]<9:
            stat_driving_period[j,9]=1
        elif ddata_driving[j,13]>17 and ddata_driving[j,14]<19:
            stat_driving_period[j,9]=2
        else:
            stat_driving_period[j,9]=0  
            
    #速度///早晚高峰车速特征（分工作日和周末）
    stat_driving_period[:,4]=stat_driving_period[:,2]/stat_driving_period[:,3]
    #行程开始、结束soc特征
    stat_driving_period[:,5]=ddata_driving[:,5]
    stat_driving_period[:,6]=ddata_driving[:,6]
    #电池能量 #使用燃油量 #里程 #soc变化
    stat_driving_period[:,7],stat_driving_period[:,8],c,d=consumptionana.ct2(ddata,datareinx)
    #日车辆出行时刻的具体分布数据，BEV、PHEV周末车辆出行时刻的分布直接结论
    stat_driving_period[:,10]=ddata_driving[:,13]
    
###日均
    day_index=np.unique(ddata_driving[:,0])
    k=0
    day_mile=0
    day_out_count_time=0
    day_driving_during=0
    for i in day_index:
        a=np.where(stat_driving_period[:,0] == i)
        for j in range(a[0].size):
            
            #日均行驶里程分布；BEV、PHEV周末日均行驶里程分布
            day_mile=day_mile+stat_driving_period[a[0][j],2]
            #日均出行次数；BEV、PHEV周末日均出行次数
            day_out_count_time=a[0].size
            #日均行驶时长；BEV、PHEV周末日均行驶时长
            day_driving_during=day_driving_during+stat_driving_period[a[0][j],3]

        stat_driving_day[k,0]=i
        stat_driving_day[k,1]=stat_driving_period[a[0][j],1]
        stat_driving_day[k,2]=day_mile
        stat_driving_day[k,3]=day_out_count_time
        stat_driving_day[k,4]=day_driving_during
        k=k+1
        day_mile=0
        day_out_count_time=0
        day_driving_during=0
#出行od热力图？    
        
        
####用户充电特征：   
    ddata_charging=ddata[ddata[:,1]==2] 
    stat_charging_period=np.zeros((ddata_charging.shape[0],7))  #每次
    stat_charging_day=np.zeros((np.unique(ddata_charging[:,0]).shape[0],3))  #每天
    stat_charging_week=np.zeros((np.unique(ddata_charging[:,0]).shape[0],4))  #每周
    
    
    stat_charging_period[:,0]=ddata_charging[:,0]#0:第几天；
    for j in range(ddata_charging.shape[0]):
        if ddata_charging[j,12]>5:
             stat_charging_period[j,1]=1 #周末
        else:
             stat_charging_period[j,1]=0 #工作日
    ##充电开始、结束soc；
    stat_charging_period[:,2]=ddata_charging[:,5]
    stat_charging_period[:,3]=ddata_charging[:,6]
    #每次充入的soc；
    stat_charging_period[:,4]=stat_charging_period[:,2]-stat_charging_period[:,1]
    #次均充电时长特征分析:
    stat_charging_period[:,5]=ddata_charging[:,4]/60
    #充电时刻与出行时刻分布对比
    stat_charging_period[:,6]=ddata_charging[:,13]
    
    
    
    
###日均
    day_index=np.unique(ddata_charging[:,0])
    k=0
    day_charge_time=0
    for i in day_index:
        a=np.where(stat_charging_period[:,0] == i)
        for j in range(a[0].size):
            
            #日充电频率；周充电频率；
            day_charge_time=a[0].size

        stat_charging_day[k,0]=i
        stat_charging_day[k,1]=stat_charging_period[a[0][j],1]
        stat_charging_day[k,2]=day_charge_time
        k=k+1
        day_charge_time=0


#充电地点热力图？
    
    
    
    
    return stat_driving_period,stat_driving_day,stat_charging_period,stat_charging_day
    
    
def statis(ddata,datareinx):  
    stat_driving_period,stat_driving_day,stat_charging_period,stat_charging_day=stat(ddata,datareinx)
    
    weekday_stat_driving_period=stat_driving_period[stat_driving_period[:,1]==0]
    weekend_stat_driving_period=stat_driving_period[stat_driving_period[:,1]==1]
    weekday_stat_driving_day=stat_driving_day[stat_driving_day[:,1]==0]
    weekend_stat_driving_day=stat_driving_day[stat_driving_day[:,1]==0]
    
    #工作日次均行驶里程分布；BEV、PHEV周末次均行驶里程分布
    period_vmt=np.mean(stat_driving_period[:,2])
    weekday_period_vmt=np.mean(weekday_stat_driving_period[:,2])
    weekend_period_vmt=np.mean(weekend_stat_driving_period[:,2])
    
    #BEV、PHEV工作日次均行驶时长；BEV、PHEV周末次均行驶时长
    period_driving_time=np.mean(stat_driving_period[:,3])
    weekday_period_driving_time=np.mean(weekday_stat_driving_period[:,3])
    weekend_period_driving_time=np.mean(weekend_stat_driving_period[:,3])
    
    #行程开始、结束soc特征
    period_start_soc=np.mean(stat_driving_period[:,6])
    weekday_period_start_soc=np.mean(weekday_stat_driving_period[:,6])
    weekend_period_start_soc=np.mean(weekend_stat_driving_period[:,6])
    
    period_end_soc=np.mean(stat_driving_period[:,7])
    weekday_period_end_soc=np.mean(weekday_stat_driving_period[:,7])
    weekend_period_end_soc=np.mean(weekend_stat_driving_period[:,7])
    
    
    
    #BEV、PHEV工作日日均行驶里程分布；BEV、PHEV周末日均行驶里程分布
    day_vmt=np.mean(stat_driving_day[:,2])
    weekday_day_vmt=np.mean(weekday_stat_driving_day[:,2])
    weekend_day_vmt=np.mean(weekend_stat_driving_day[:,2])
    
    #BEV、PHEV工作日日均出行次数；BEV、PHEV周末日均出行次数
    day_outtime=np.mean(stat_driving_day[:,3])
    weekday_day_outtime=np.mean(weekday_stat_driving_day[:,3])
    weekend_day_outtime=np.mean(weekend_stat_driving_day[:,3])
    
    #BEV、PHEV工作日日均行驶时长；BEV、PHEV周末日均行驶时长
    day_driving_time=np.mean(stat_driving_day[:,4])
    weekday_day_driving_time=np.mean(weekday_stat_driving_day[:,4])
    weekend_day_driving_time=np.mean(weekend_stat_driving_day[:,4])
    
    
    #早晚高峰车速特征（分工作日和周末）行程开始结束都在am7-9；pm5-7
    period_speed=np.mean(stat_driving_period[:,5])
    weekday_period_speed=np.mean(weekday_stat_driving_period[:,5])
    weekend_period_speed=np.mean(weekend_stat_driving_period[:,5])
    
    #工作日早晚高峰车速
    ampeak_weekday_stat_driving_period=weekday_stat_driving_period[weekday_stat_driving_period[:,1]==1]
    nonpeak_weekday_stat_driving_period=weekday_stat_driving_period[weekday_stat_driving_period[:,1]==0]
    pmpeak_weekday_stat_driving_period=weekday_stat_driving_period[weekday_stat_driving_period[:,1]==2]
    
    #周末早晚高峰车速
    ampeak_weekend_stat_driving_period=weekend_stat_driving_period[weekend_stat_driving_period[:,1]==1]
    nonpeak_weekend_stat_driving_period=weekend_stat_driving_period[weekend_stat_driving_period[:,1]==0]
    pmpeak_weekend_stat_driving_period=weekend_stat_driving_period[weekend_stat_driving_period[:,1]==2]
    
    #工作日早晚高峰车速
    ampeak_weekday_period_speed=np.mean(ampeak_weekday_stat_driving_period[:,5])
    nonpeak_weekday_period_speed=np.mean(nonpeak_weekday_stat_driving_period[:,5])
    pmpeak_weekday_period_speed=np.mean(pmpeak_weekday_stat_driving_period)
    
    #周末早晚高峰车速                            
    ampeak_weekend_period_speed=np.mean(ampeak_weekend_stat_driving_period[:,5])
    nonpeak_weekend_period_speed=np.mean(nonpeak_weekend_stat_driving_period[:,5])
    pmpeak_weekend_period_speed=np.mean(pmpeak_weekend_stat_driving_period)
    
    
    
    #BEV、PHEV工作日车辆出行时刻的具体分布数据，BEV、PHEV周末车辆出行时刻的分布直接结论
    
    
    #出行od热力图？

##用户充电特征：
    ##日充电频率；周充电频率；(pic)
    day_charge_times=np.mean(stat_charging_day[:,2])
    period_charge_time=np.mean(stat_charging_period[:,5])
    #单次充电时长(pic)
    #充电开始、结束soc；(pic)
    charging_start_soc=np.mean(stat_charging_period[:,2])
    charging_end_soc=np.mean(stat_charging_period[:,3])
    #每次充入的soc；
    charged_soc=np.mean(stat_charging_period[:,4])
    #充电时刻与出行时刻分布对比、(pic)
    #充电地点热力图？

    return period_vmt,weekday_period_vmt,weekend_period_vmt,period_driving_time,weekday_period_driving_time,weekend_period_driving_time,\
        period_start_soc,weekday_period_start_soc,weekend_period_start_soc,period_end_soc,weekday_period_end_soc,weekend_period_end_soc,\
        day_vmt,weekday_day_vmt,weekend_day_vmt,day_outtime,weekday_day_outtime,weekend_day_outtime,day_driving_time,weekday_day_driving_time,\
        weekend_day_driving_time,period_speed,weekday_period_speed,weekend_period_speed,ampeak_weekday_period_speed,nonpeak_weekday_period_speed,\
        pmpeak_weekday_period_speed,ampeak_weekend_period_speed,nonpeak_weekend_period_speed,pmpeak_weekend_period_speed,day_charge_times,\
        period_charge_time,charging_start_soc,charging_end_soc,charged_soc
        
        
        
        
##研究相关性：宏观方面的        
        
filename='phev_stat.csv'
data=pd.read_csv(filename)
aa=data.corr()

