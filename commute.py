# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 13:32:14 2018

@author: anita
"""
import pandas as pd
import numpy as np
import location_search
import park_period
import time
import datetime

def re_idx1(datareinx,timeser):

    
    #输入：原数据表dataframe，出行表addata
    #输出：对addata第一列数据的索引修正re_index
    #re_index是shape为addata.shape[0]行，1列的索引标识
    re_index=np.zeros((timeser.shape[0],1))
    time_collect=datareinx['time_collect']
    date0=time_collect[0]
    date0=time.strptime(date0,"%Y-%m-%d %H:%M:%S")
    date0=datetime.datetime(date0[0],date0[1],date0[2],0,0,0)
    for i in range(len(timeser)):
        date1=time.strptime(timeser[0],"%Y-%m-%d %H:%M:%S")
        date1=datetime.datetime(date1[0],date1[1],date1[2],0,0,0)
        re_index[i]=(date1-date0).days
    
    return re_index


def strip_day(timeStra):
    """
    返回的是小时
    """
    H = timeStra.days
    
    return H




def commutetab(ddata,datareinx):
    t_c=datareinx['time_collect']
    t_c=pd.to_datetime(t_c)
    t_c0=t_c[0]
    llw,llh=park_period.pp2(datareinx)  #找到了白天和晚上的长时间停留的地点
    if len(llw)==0 or len(llh)==0:
        charginwper,charginhper,nw,nh,ucw,work_place,home_place=0,0,0,0,0,0,0
    else:

        aawr,nw=location_search.locatsearch(llw)  #一串经纬度序列，返回最为聚集的一个位置以及其聚集的百分比,经纬度序列是panda的dataframe形式
        aahr,nh=location_search.locatsearch(llh)
        work_place=aawr.iloc[0]  #取出第一个位置
        home_place=aahr.iloc[0]
    
    
    
        w_inx=aawr.index.tolist() #将数组或者矩阵转换成列表
        h_inx=aahr.index.tolist()
        tw=t_c[w_inx]   #找到这些位置的时间
        th=t_c[h_inx]
    
    
        dw=(tw-t_c[0]).apply(strip_day)   #apply：应用某个def；  strip_day：返回的是小时；和第一个时间相比中间间隔了多久小时
   # dh=(th-t_c[0]).apply(strip_day)
        cw=np.array(dw)
        ucw=np.unique(cw)
    #for i in range 
    
    
        cou=0
    
    
        for i in range (len(w_inx)):
        
            ddata1=ddata[ddata[:,1]==1]
            ddata2=ddata1[ddata1[:,2]>w_inx[i]]
            if len(ddata2)==0:
                continue
            else:
        
                if ddata2[0,5]-datareinx['quqantity_electricity_percent'].iloc[int(w_inx[i])]>15:
                    cou=cou+1
        #print(len(w_inx),nw,cou)
        charginwper=cou/len(w_inx)
        
        
        cou=0
        for i in range (len(h_inx)):
        
            ddata1=ddata[ddata[:,1]==1]
            ddata2=ddata1[ddata1[:,2]>h_inx[i]]
            if len(ddata2)==0:
                continue
            else:
        #print(ddata2[0,2],h_inx[i])
        #print(ddata2[0,5],datareinx['quqantity_electricity_percent'].iloc[int(h_inx[i])])
                if ddata2[0,5]-datareinx['quqantity_electricity_percent'].iloc[int(h_inx[i])]>15:
                    cou=cou+1
        charginhper=cou/len(h_inx)
        
        
    return charginwper,charginhper,nw,nh,ucw,work_place,home_place
##到工作地+充电的比例，到家+充电的比例，到家的记录，到工作地的记录，通勤天数的记录，工作地点，家庭地点

#aa=aawr.index.tolist()
##
#    t=datareinx['time_collect'][w_inx]
#    t=pd.to_datetime(t)
    
    
    
    
    ##判断是否有家充电机会：
    

