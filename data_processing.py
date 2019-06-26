# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:46:33 2018

@author: XPS
"""


import pandas as pd

def loadData1(filename):
    with open(filename) as txtData:
        lines=txtData.readlines()
        line=lines[0]
    with open(filename,'r+') as f:
        content=f.read()
        a=content
        f.seek(0,0)
        f.write(line)
        f.write(content)
    df=pd.read_csv(filename,sep=',')
    x=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,27,28,33,34,35,36,37,38,39,40,41,42,43,46]
    df.drop(df.columns[x],axis=1,inplace=True)
    column=['time_collect','distance_accumulative','longitude_we',\
            'status_location','latitude_ns','longitude','latitude',\
            'speed','orientation','temperature_controller',\
            'rotateapeed_drive','temperature_drive','isbreak',\
            'status_powersystem','quqantity_electricity_percent',\
            'quqantity_electricity','time_start','fuel_consumption',\
            'time_stall','current_status_vehicle']
    df.columns=column
    with open(filename,'w') as w:
        for k in lines:
            w.write(k)

    return df

def loadData2(filename):
    Data=[]
    with open(filename) as txtData:
        lines=txtData.readlines()
        for line in lines:
            lineData=line.strip().split(',')
            Data.append(lineData)
    df=pd.DataFrame(Data)
    x=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,27,28,33,34,35,36,37,38,39,40,41,42,43,46]
    df.drop(df.columns[x],axis=1,inplace=True)
    column=['time_collect','distance_accumulative','longitude_we',\
            'status_location','latitude_ns','longitude','latitude',\
            'speed','orientation','temperature_controller',\
            'rotateapeed_drive','temperature_drive','isbreak',\
            'status_powersystem','quqantity_electricity_percent',\
            'quqantity_electricity','time_start','fuel_consumption',\
            'time_stall','current_status_vehicle']
    df.columns=column
    return df,Data
        
def loadData3(filename):
#    filename=fp
    df=pd.read_csv(filename,sep=',',encoding='gb2312')
    if len(df)==0:
        a=0
    else:
        
    #数据采集时间,累积行驶里程,定位状态,东经.西经,北纬.南纬,经度,
    #纬度,方向,速度,电机控制器温度,驱动电机转速,驱动电机温度,
    #电机母线电流12,加速踏板行程13,制动踏板状态,动力系统就绪,电池剩余电量(SOC),电池剩余能量,
    #高压电池电流,电池总电压,单体最高温度20,单体最低温度21,单体最高电压22,单体最低电压23,
    #绝缘电阻值24,电池包最高温度25,电池包最高温度_1 26,电池包最低温度27,电池包最低温度_1 28,电池均衡激活29,
    #紧急下电请求30,启动时间,液体燃料消耗量,上下线状态33,熄火时间,车辆当前状态
    ##删除12和18
        x=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,27,28,36,37,38,39,40,41,42,43,46]
        #x=[12,13,20,21,22,23,24,25,26,27,28,29,30,33] 师姐
        df.drop(df.columns[x],axis=1,inplace=True)
#        column=['time_collect','distance_accumulative','status_location',\
#                'longitude_we','latitude_ns','longitude','latitude',\
#                'orientation','speed','temperature_controller',\
#                'rotateapeed_drive','temperature_drive','isbreak',\
#                'status_powersystem','quqantity_electricity_percent',\
#                'quqantity_electricity','current','volt',\
#                'time_start','fuel_consumption',\
#                'time_stall','current_status_vehicle'] 师姐
        column=['time_collect','distance_accumulative','longitude_we',\
                'status_location','latitude_ns','longitude','latitude',\
                'speed','orientation','temperature_controller',\
                'rotateapeed_drive','temperature_drive','isbreak',\
                'status_powersystem','quqantity_electricity_percent',\
                'quqantity_electricity','current','volt','high_temperature',\
                'time_start','fuel_consumption',\
                'time_stall','current_status_vehicle']
        df.columns=column
#        time=df.pop('time_collect')
#        df.insert(0,'time_collect2',time)
#        df.insert(0,'time_collect',time)
#        
    
    return df