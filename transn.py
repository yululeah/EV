# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:13:49 2018

@author: anita
"""

#对停留段的修正

#对于datacleaning以外的都设为非行程段（或者看是否均为充电段）
import pandas as pd
import numpy as np
import getTimeDiff
import latlon
import data_analysis
#import matplotlib.pyplot as plt
##


#简单的数据清洗
def datacleaning(data):
    #data=data[data['distance_accumulative']>0]
    data=data[data['longitude']>0]
    data=data[data['latitude']>0]
    data=data[data['current_status_vehicle']!=-1]
    data=data[data['distance_accumulative']<=1000000]
    d_c=np.array(data['distance_accumulative'])
    lon=np.array(data['longitude'])
    lat=np.array(data['latitude'])
    for i in range(d_c.shape[0]):
        if d_c[i]==0:  #对于数据缺失的
            d_c[i]=d_c[i-1]+latlon.haversine(lon[i-1],lat[i-1],lon[i],lat[i])/1000#补全车公里

    d_c=d_c.astype(int)  #转化为整数
    
###删除可能存在的跳跃的里程数据
    
    dcc=pd.Series(d_c, index=list(data.index))
    data['distance_accumulative']=dcc
    
    t_c=data['time_collect']
    d_c=data['distance_accumulative']
    timed=np.ones((t_c.shape[0],))
    timed=pd.Series(timed,index=list(t_c.index))
    dd=np.zeros((t_c.shape[0],))
    dd=pd.Series(dd, index=list(t_c.index))
    t_cu=t_c.shift(-1)
    d_cu=d_c.shift(-1)
    for i in list(t_c.index)[0:-1]: ###关注一下apply   ##[0:-1]表示第一个元素到倒数第二个元素的切片

        timed[i]=getTimeDiff.GetTimeDiff(t_c[i],t_cu[i])
        if timed[i]>50*60: #如果说开始出现时间的跳跃
            timed[i]=1e20
            dd[i]=d_cu[i]-d_c[i] #里程差值
        else:
            dd[i]=d_cu[i]-d_c[i]

    spd=dd/timed * 1e3
    data['newspd']=spd  #新增一列计算速度，代表该时刻与下时刻里程差值与时间差值的比值，单位为m/S，区分E-20左右时有时间的跳跃    
    
    return data
#timestamp cal
#def timest(data): 
#    t_c=data['time_collect']
#    g=np.zeros((t_c.shape[0],))
#    time_acc=pd.Series(g, index=list(t_c.index))
#    for i in list(t_c.index):
#        time_acc[i]=getTimeDiff.GetTimeDiff(t_c[list(t_c.index)[0]],t_c[i])
#    return time_acc


    
#def select(df1): 
#    import getTimeDiff 
#    import numpy as np
#    import pandas as pd
#     ##仅处理行程段
#    d_c=df1['distance_accumulative']
#    t_s=timest(df1)
#    d_t_s=pd.concat([t_s,d_c],axis=1)
#    return d_t_s


def stop(dada):
    import numpy as np
    import pandas as pd
    #dada=dada[dada['current_status_vehicle']==1]
    
    ds=dada['distance_accumulative'].shift(-1)
    dsmda=ds-dada['distance_accumulative']   #里程差
    
    dsmdaa=np.array(dsmda)
    st=np.zeros((dsmdaa.shape[0],))
    
    timestr=pd.to_datetime(dada['time_collect']) #转化为时间格式
    timest=timestr.reset_index(drop=True) #序号重新排列
    i=0
    while i<dsmdaa.shape[0]-1:
        if dsmdaa[i]==0:  #如果里程差是0
            j=i
            while dsmdaa[j]==0:
                j=j+1 #直到里程差不为0时跳出循环，即找到里程跳动的节点
            if (timest[j]-timest[i]).total_seconds()>20*60:# and abs(soca[i]-soca[j])<10 :##设置停留时间大于15分钟则作为停留段落
                st[i:j]=188
                i=j-1
            else:
                i=j-1
        i=i+1
    st=pd.Series(st, index=list(dada.index))
    stc=st[st!=0]
    dwellinx=list(stc.index)
    return dwellinx   #输出停留20分钟以上的index

def datac(data1): #data1为raw data
    
    data1['latitude']=data1['latitude']/1e6
    data1['longitude']=data1['longitude']/1e6
    data=datacleaning(data1)

#    dada1=data.reset_index()
    dewllinx=stop(data)
     #针对长时间停留的处理，提取出index
    data['status_basic']=data['current_status_vehicle']
    data['current_status_vehicle'][dewllinx]=0  #将符合长时间停留（20min）的status赋值为0 
    datareinx=data.reset_index()
    datar2=data_analysis.status102(datareinx)  #将时间超过10分钟，里程不变的status赋值为2
#    oldinx=datareinx['index']
    
    
    ddata=data_analysis.trip(datar2)
#    d2=np.array(oldinx[ddata[:,2]])
#    d3=np.array(oldinx[ddata[:,3]])
#    ddata[:,2]=d2
#    ddata[:,3]=d3 #替换变为顺序编码后的index
#    addata=ddata[ddata[:,4]!=0]
    return ddata,datareinx     
            
        