#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 21:04:47 2019
有多少比例是由于充电时间不够长导致的用油（15min前是在充电，但是没有90%以上）
有多少是由于里程超出range而用油？（从90%以上的电量开始）
有多少比例是没有机会充电导致的用油？
@author: apple
"""


def why_fuel(ddata,datareinx):
    import getTimeDiff
    import numpy as np
    data=np.zeros((1,15))
    categary1=0#由于充电时间不够长导致的用油（15min前是在充电，但是没有90%以上）
    categary2=0#由于里程超出range而用油？（从90%以上的电量开始）
    categary3=0#没有机会充电导致的用油？上一个行程距此很远，但是没有机会充电？
    categary4=0#总用油行程数

    qep=datareinx['quqantity_electricity_percent']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']
    
    for i in range(1,ddata.shape[0]):
        a=int(ddata[i,2]) #索引
        b=int(ddata[i,3]) #索引
        
        
        '''判断是不是烧油的行程段'''
        if any(fc.loc[a+1:b]>500) and ddata[i,1]==1 and ddata[i,6]<=20 :  #大于500就是在烧油驱动
            categary4=categary4+1
            data=np.vstack((data,ddata[i,:]))
            
            #由于充电时间不够长导致的用油（15min前是在充电，但是没有90%以上）
            if datareinx['statusn2'].loc[int(ddata[i-1,3])]==102 and getTimeDiff.GetTimeDiff(tc.loc[(ddata[i-1,3])],tc.loc[a])/60 <=15  and qep.loc[a]<90 :
                categary1+=1
            #由于里程超出range而用油？（从90%以上的电量开始）
            elif qep.loc[a]>=90:
                categary2+=1
            #没有机会充电导致的用油？上一个行程距此很久远，但是没有机会充电？
            elif getTimeDiff.GetTimeDiff(tc.loc[(ddata[i-1,3])],tc.loc[a])/60 >45:
                categary3+=1
            

    return categary1,categary2,categary3,categary4
    