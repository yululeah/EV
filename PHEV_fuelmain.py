# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 06:36:25 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import time
import os
import cleanfuel
import olsan
import consumptionana
import comsumption
import whyfuel
import fourmode
import calorific_value

path1=r'/Users/apple/Desktop/研一/research_on_EV/data/hybrid16/'
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

consump_fuel=np.zeros((1,6))##记录每个行程/cs模式
consump_elec=np.zeros((1,6))##记录每个行程/cd模式
data_divert_tab=np.zeros((1,7))##记录每5min
p_tab=[]

j1=np.zeros((600,8))##记录能耗的各项参数
time_start=time.time()
#num=0
for i in range (1,len(file_list)):
    filename1='/Users/apple/Desktop/研一/research_on_EV/data/ddatac/phev/ddatac'+str(i)+'.csv'
    filename2='/Users/apple/Desktop/研一/research_on_EV/data/datareinx/phev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/研一/research_on_EV/data/phev/ddatac'
#    filename1='D:/1/72282/ddata2c'+str(i)+'.csv'
#    filename2='D:1/72282/datareinx'+str(i)+'.csv'
#    path='D:/1/72282'
    if os.path.exists(filename1)==True:
        
        ddata=np.array(pd.read_csv(filename1))
        datareinx=pd.read_csv(filename2)
#        num=num+len(ddata[ddata[:,1]==1])
        ###每5min
#        data_divert,p=fourmode.mode(ddata,datareinx) #提取油电混动
#        p_tab.append(p)  #获取油电比
#        data_divert=calorific_value.calorific_value2(data_divert,p) #计算速度和热值
        Epure,p=fourmode.mode(ddata,datareinx) #提取纯电
        p_tab.append(p)
        
#        ddata=cleanfuel.task3(datareinx,ddata) #清洗
# =============================================================================
# 计算pdf
#        if len(ddata[ddata[:,1]==1])==0:
#            continue
#        else:
#            aa=olsan.fresult(ddata,datareinx)
#            if aa:
#                j1[i,0]=aa[0]###soc的t值
#                j1[i,1]=aa[1]###耗油量的t值
#                j1[i,2]=aa[2]###soc的coef
#                j1[i,3]=aa[3]##
#                j1[i,4]=aa[4]###电里程比例1
#                j1[i,5]=aa[5]###电里程比例2
#                #j1[i,6]=aa[2]*aa[8]/aa[9]
#                #sce,sy=olsan.frec(data,datareinx)
#                #cper=sce*aa[2]/sy
#                #j1[i,6]=cper
#                j1[i,6]=aa[10] #用热值做的pdf
# 
# =============================================================================
        ###研究里程、时间、耗电、耗油之间的关系
#        dg=consumptionana.ct2(ddata,datareinx)
#        consump_fuel_temp = np.vstack((np.array(dg[0]),np.array(dg[1]),np.array(dg[2]),np.array(dg[3]),np.array(dg[4]),np.array(dg[5])))
#        consump_fuel_temp=np.transpose(consump_fuel_temp)
#        consump_fuel = np.vstack((consump_fuel,consump_fuel_temp))
#        
#        consump_elec_temp = np.vstack((np.array(dg[6]),np.array(dg[7]),np.array(dg[8]),np.array(dg[9]),np.array(dg[10]),np.array(dg[11])))
#        consump_elec_temp=np.transpose(consump_elec_temp)
#        consump_elec = np.vstack((consump_elec,consump_elec_temp))
        
        
#        data_divert_tab=np.vstack((data_divert_tab,data_divert))
        
# =============================================================================
#探究用油的原因
#        wf.append(whyfuel.why_fuel(ddata,datareinx))
        
# =============================================================================
    print(i)
    print(time.time()-time_start)
    
    c=calorific_value.calorific_value3(data_divert_tab)
    
    
    ##cs mode 剔除soc小于0的：
    consump_elec = np.delete(consump_elec,np.where(consump_elec[:,3]<=0),axis=0)
    ##cd mode 剔除soc大于3的：
    consump_fuel = np.delete(consump_fuel,np.where(consump_fuel[:,3]>=3),axis=0)
    #删除行程为0的
    consump_elec = np.delete(consump_elec,np.where(consump_elec[:,1]<=0),axis=0)
    consump_fuel = np.delete(consump_fuel,np.where(consump_fuel[:,1]<=0),axis=0)
    data_divert_tab=np.delete(data_divert_tab,np.where(data_divert_tab[:,1]==0),axis=0)
    
def savedd(data,fstr):
    aa=pd.DataFrame(data)
    name='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/store/phev_'+fstr+'.csv'
    aa.to_csv(name,index=False)
    
savedd(j1,'olsa_result')


