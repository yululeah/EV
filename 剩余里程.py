#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:24:10 2019

@author: apple

师姐：找就是BEV的数据里面，看一下电量剩余60% 40% 20%的时候对应的剩余里程一般是多少？
应该是看降低的过程的
就是比如说车上显示50%的时候
剩余多少里程
"""


import numpy as np
import pandas as pd
import time
import os
import statsmodels.api as sm

def olsa(x,y):
    est = sm.OLS(y,x).fit()
    para=est.params 
      
    return para 



def rsquared(x, y):
    import scipy
    """ Return R^2 where x and y are array-like."""
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2


path1=r'/Users/apple/Desktop/shakalaka/电动车行为研究/数据/bev16/'
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

#table_1=np.zeros((103,104))
time_start=time.time()
names=locals()
st=np.ones((0,13))
para_tab=np.arange(1)



for i in range (1,len(file_list)):
    data10_60=np.zeros((1000,15))
    filename1='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/ddatac/bev/ddatac'+str(i)+'.csv'
    filename2='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/datareinx/bev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/bev/ddatac'
#    filename1='D:/1/bevdata2/ddatac'+str(i)+'.csv'
#    filename2='D:/1/bevdata2/datareinx'+str(i)+'.csv'
#    path='D:/1/bevd2ata'
    if os.path.exists(filename1)==True:
        
        ddata=np.array(pd.read_csv(filename1))
        datareinx=pd.read_csv(filename2)
#        ddata_tab=pd.concat([ddata_tab,pd.DataFrame(ddata)],axis=0,ignore_index=True)
    
    
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']

    
    data10_60=ddata[ddata[:,1]==1]
    data10_60=data10_60[data10_60[:,5]-data10_60[:,6]>30]
#    data10_60=data10_60[data10_60[:,5]>60]
#    data10_60=data10_60[data10_60[:,6]<11] #确定是线性的了
    

    for j in range (data10_60.shape[0]):
        a=int(data10_60[j,2]) #索引
        b=int(data10_60[j,3]) #索引
        cc=np.zeros((b-a+1,2))
        kk=0
        for k in range(a,b+1):
            if qep.loc[k]>qep.loc[k+1]:
                cc[kk,0]=qep.loc[k]
                cc[kk,1]=da.loc[k]
                kk=kk+1
                
#                cc_temp_temp=cc[kk-1,1]+cc[kk-1,0]
#                cc_temp1=np.array([[0, cc_temp_temp]])
#                cc = np.row_stack((cc, cc_temp1))
                
#                cc_temp2_temp = np.array([[0]])
        cc=cc[cc[:,0]!=0]
        index_start= 0
        index_end=len(cc)
        if index_end>=3:
            y=cc[1:index_end,1]-cc[0:index_end-1,1] #距离
            x=cc[0:index_end-1,0]-cc[1:index_end,0] #soc
            para=olsa(x,y)
#            if rsquared(x,y)>0.7:
            para_tab=np.hstack((para_tab,para[0]))
                
para_tab=np.delete(para_tab,0)


#正态分布曲线

import matplotlib.mlab as mlab 
import matplotlib.pyplot as plt 

mu =np.mean(para_tab) #计算均值 
sigma =np.std(para_tab) 
num_bins = 22 #直方图柱子的数量 
n, bins, patches = plt.hist(para_tab, num_bins,normed=1, facecolor='blue', alpha=0.5) 
#直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象 
y = mlab.normpdf(bins, mu, sigma)#拟合一条最佳正态分布曲线y 
plt.plot(bins, y, 'r--') #绘制y的曲线 
plt.xlabel('parameter') #绘制x轴 
plt.ylabel('Probability') #绘制y轴 
#plt.title(r'Histogram : $\mu=5.8433$,$\sigma=0.8253$')#中文标题 u'xxx' 
#plt.subplots_adjust(left=0.15)#左边距 
plt.show()

