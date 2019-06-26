#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:20:09 2019

改进版consumptionana 
只选取fuel_consumption从0开始的段
@author: yulu
"""

import numpy as np
import modified_trip
import getTimeDiff

def modified_ct(ddata,datareinx):
    
    
    #先处理index和“index”不符合的情况
#    datareinx=datareinx[datareinx['index']<datareinx.shape[0]]
    datareinx['index']=datareinx.index
    
    data=np.zeros((1,16))
    ##
    data_divert_T=np.zeros((1,4))
    T=5 #时间间隔
    
    
    datereinx_temp=datareinx[datareinx['fuel_consumption']==0]
#    datereinx_temp=datereinx_temp[datereinx_temp['status_basic']==1]
    if datereinx_temp.shape[0]!=0:
        
        index=np.array(datereinx_temp['index'])
        index_2=[] #放入燃油从0到非0 的全部索引
        for i in range(1,len(index)-1):
#            if index[i] in datereinx_temp['index'] and index[i+1] in datereinx_temp['index']:
            if datereinx_temp['index'].loc[index[i]]+1<datereinx_temp['index'].loc[index[i+1]]:
                index_2.append((datereinx_temp['index'].loc[index[i]],datereinx_temp['index'].loc[index[i+1]]))
#            else:
#                continue
        if (datareinx.shape[0]-1) not in index_2:
            index_2.append((index[-1],datareinx.shape[0]-1))
        
# =============================================================================
########提取纯用电的
#     #    ddata_0_temp=np.zeros((1,15))
#     #    for i in range(len(ddata)):
#     #        if ddata[i,2] in index:
#     #            ddata_0_temp=np.vstack((ddata_0_temp,ddata[i,:]))
#     #
#     #    ddata_0_temp=np.delete(ddata_0_temp,[0],axis=0)
#     #    cg=consumptionana.ct(ddata_0_temp,datareinx)
#     #    ce=np.array(cg[1])/1000 ##使用的燃油量‘
#     #
#     ##矩阵中添加行：numpy.row_stack(mat, a)
#     ##矩阵中添加列：numpy.column_stack(mat,a)
#     #    
#     #    ddata_0_temp=np.column_stack((ddata_0_temp,ce))
#     #    ddata_pure_electricity=ddata_0_temp[ddata_0_temp[:,15]==0,:]
#     #    temp1=np.array(datareinx['quqantity_electricity'].loc[ddata_pure_electricity[:,2]])
#     #    temp2=np.array(datareinx['quqantity_electricity'].loc[ddata_pure_electricity[:,3]])
#     #    ddata_pure_electricity[:,15]=temp1-temp2 #消耗的quqantity_electricity
# =============================================================================
        
        #######用油的
    #从燃油消耗量为0的地方开始计算，下一个燃油量减上一个
    #当100km以上时，
    #如果下一个行程和上一个行程之间的distance_accumulate大于30？，停止，从下一个为0 的开始
    #或者一直进行到fuel为0，该段行程舍去
    
         
        da=np.array(datareinx['distance_accumulative'])
        fc=np.array(datareinx['fuel_consumption'])
        
        
        
        for i in range(len(index_2)):
            index_start=index_2[i][0]
            index_end=index_2[i][1]
            
            
            
            
            #前100公里
            datareinx_temp=datareinx.iloc[index_start:index_end]  #从index_start到index_end；前闭后闭
            
            #判断是否存在fuel_consumption跳跃的点
            fc=datareinx_temp['fuel_consumption']
            fca=fc.loc[index_start+1:index_end].reset_index(drop=True) 
            fcu=fc.loc[index_start:index_end-1].reset_index(drop=True) 
            fcminus=fca-fcu
            ##找到第一个跳跃的点，往后全部舍弃
            fcminus=fcminus[fcminus>20]
            if len(fcminus)>0: #如果存在，舍弃后面的，重新赋值
                index_end=fcminus[fcminus == fcminus.iloc[0]].index.tolist()
                index_end=index_end[0]+index_start
                datareinx_temp=datareinx.iloc[index_start:index_end]  #从index_start到index_end；前闭后闭
                
                
                
            ##增加一列累计燃油
            datareinx_temp['fuel_accumulate']=0
            distance_accumulate_start=np.array(datareinx['distance_accumulative'].loc[index_start])
            distance_accumulate_100=distance_accumulate_start+100 #找100km开外的公里数
            distance_accumulate_start=distance_accumulate_100-100 #找开始的公里数
            
            #找100km开外的公里数的index
            index_100 = datareinx[datareinx.distance_accumulative == distance_accumulate_100].index.tolist() # index
            
            if len(index_100)>0: #要是找到了
                index_100=index_100[0]
            else:  #要是没找到，找最近的那个
                x=distance_accumulate_100
                a=abs(da-x)
                b=a.min()
                 ###还是要用插值法？？
                if b>10: #(距离小于10) 要是找到最近的那个了，但是它大于10km远，我们就不找了，索引的end
                    index_100=index_end+1 #为了创造条件，使得下面一块运行if后面的语句
                else:
                    c=abs(x-b)  #最近里程的数字
                    index_100 = datareinx[datareinx.distance_accumulative == c].index.tolist() # index
                    if len(index_100)==0:
                        c=abs(x+b)  #最近里程的数字
                        index_100 = datareinx[datareinx.distance_accumulative == c].index.tolist() # index
                    index_100=index_100[0] #第100公里所在的行号index
            
                
            #如果第100公里所在的行号index超过了index_end
            if index_100>index_end: 
                datareinx_temp['fuel_accumulate'].loc[index_start:index_end]=fc[index_start-index_start:index_end+1-index_start]
            else: #如果没超过
                datareinx_temp['fuel_accumulate'].loc[index_start:index_100]=fc[index_start-index_start:index_100+1-index_start]
                    
                 #100公里外的
                j=index_100
                while j <index_end:
                    index_self = np.where(da==da[j]) #本身的最后一个值
                    index_self = index_self[0][-1]
                    index_temp = np.where(da==da[j]-100) # index  #找100公里之前的那个数字
                    #if fc[j]!=0:
                    if len(index_temp[0])!=0:
                         #100km之前的那个索引
                        k=-1
                        index_temp_1 = index_temp[0][k]
                        while index_temp_1>index_end:  #避免有一些里程不规律，出现递减
                            index_temp_1 = index_temp[0][k]
                            k=k-1
                        if index_temp_1>index_start and index_temp_1<=index_end:
                            datareinx_temp['fuel_accumulate'].loc[j:index_self]=fc[index_temp_1]+fc[j]
                            
                    else:   #如果找不到的话，找最近的里程的数
                        x=da[j]-100
                        a=abs(da-x)
                        b=a.min()
                        if b<=10:
                            c=abs(x-b)  #最近里程的数字
                            index_temp_2 = np.where(da==c) # index
                            if index_temp_2[0].size==0:
                                c=abs(x+b)  #最近里程的数字
                                index_temp_2 = np.where(da==c) # index
                            index_temp_2 = index_temp_2[0][-1] #100km之前的那个索引
                            if index_temp_2>index_start:
                                datareinx_temp['fuel_accumulate'].loc[j:index_self]=fc[index_temp_2]+fc[j]
                        else:
                            break
                        
                    j=index_self+1
            data=np.vstack((data,modified_trip.trip(datareinx_temp)))
# =============================================================================
#        不同速度区间下的电动车的能耗？速度跟油耗/电耗的关系？每五分钟，算平均速度（里程/5min），
##        耗电量/耗油量/状态为1
#            datareinx_temp=datareinx_temp[datareinx_temp['statusn2']==1]
            
            k=index_start
#                for k in range((index_start,index_end)):
            while k<index_end:
                time_start=datareinx['time_collect'].loc[k]
                da_start=datareinx['distance_accumulative'].loc[k]
                qep_start=datareinx['quqantity_electricity_percent'].loc[k]
                fa_start=datareinx_temp['fuel_accumulate'].loc[k]
                
                while getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k])<T*60 and k<index_end :#如果在5分钟内
                    k=k+1
                #break出来的时候，就是找到了那个大于5分钟的值？
                
                #持续时间、路程、soc变化、燃油变化
                data_divert_T_temp=np.hstack((getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k-1]), \
                                              datareinx['distance_accumulative'].loc[k-1]-da_start, \
                                              qep_start-datareinx['quqantity_electricity_percent'].loc[k-1], \
                                              datareinx_temp['fuel_accumulate'].loc[k-1]-fa_start))
                data_divert_T=np.vstack((data_divert_T,data_divert_T_temp))
    
# =============================================================================
                
                
            
            

    data=data[data[:,15]>=0]
    data=np.delete(data,0,axis = 0)
    
    data_divert_T=data_divert_T[data_divert_T[:,0]<=(T+1)*60]#小于t+1分钟
    data_divert_T[:,0]=data_divert_T[:,0]/60 #换算成分钟
    data_divert_T=data_divert_T[data_divert_T[:,1]>0]  #路程大于0
    data_divert_T=data_divert_T[data_divert_T[:,3]>=0]
    
    return data,data_divert_T
                
