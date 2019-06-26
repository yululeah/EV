# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:58:54 2018

@author: XPS
"""

import numpy as np
import pandas as pd
#from pandas import Series
import datetime
import time
#import matplotlib.pyplot as plt
#import math
#import switchtotimearray
#import latlon
import getTimeDiff


def strip_day(timeStra):
    """
    返回的是小时
    """
    H = timeStra.days
    
    return H


def re_idx(dataframe,addata):
    #输入：原数据表dataframe，出行表addata
    #输出：对addata第一列数据的索引修正re_index
    #re_index是shape为addata.shape[0]行，1列的索引标识
    re_index=np.zeros((addata.shape[0],1))
    time_collect=dataframe['time_collect']
    date0=time_collect[0]
    date0=time.strptime(date0,"%Y-%m-%d %H:%M:%S")
    date0=datetime.datetime(date0[0],date0[1],date0[2],0,0,0)
    for i in range(addata.shape[0]):
        date1=time.strptime(time_collect[addata[i,2]],"%Y-%m-%d %H:%M:%S")
        date1=datetime.datetime(date1[0],date1[1],date1[2],0,0,0)
        re_index[i]=(date1-date0).days
    
    return re_index

def status102(dataframe):#需要对不连续的index首先进行处理
    status=dataframe['current_status_vehicle']
    q_e_p=dataframe['quqantity_electricity_percent']   
    spe=dataframe['newspd']
    time_collect=dataframe['time_collect']
    t_c=pd.to_datetime(time_collect)
    d_c=dataframe['distance_accumulative']
    lens=len(status)
    st=np.array(status)
    statusn2=pd.Series(st,index=list(status.index))

    k=0
    while k<lens-2:
        if q_e_p[k+1]-q_e_p[k]>0 and q_e_p[k+1]-q_e_p[k]<10 and spe[k+1]==0 :
            j=k
            k=k+1
            while k<lens-3:
                if q_e_p[k+1]-q_e_p[k]>0:
                    k=k+1
                if q_e_p[k+1]-q_e_p[k]==0:
                    k=k+1
                
                if q_e_p[k+1]-q_e_p[k]<0 or q_e_p[k+1]==100 or spe[k+1]!=0 or int((t_c[k+1]-t_c[k]).total_seconds())>30*60:
                    #如果下一次电量比上一次少/电量为100%/速度不为0/前后时间大于30min
                    #此时，前后时间大于10min且前后距离小于2，认为是停止状态
                    if (t_c[k]-t_c[j]).total_seconds()>10*60 and abs(d_c[j]-d_c[k])<2:
                        statusn2[j:k+1]=102
#                        while j>0:##向上寻找soc不变的开始作为充电段的开始
#                            if q_e_p[j-1]==q_e_p[j] and abs(d_c[j]-d_c[k])<1:
#                                j=j-1
#                            else:
#                                break
                              
                        #print(getTimeDiff.GetTimeDiff(time_collect[j],time_collect[k]),j,k,abs(d_c[j]-d_c[k]))
                        break
                    else:
                        break
        k=k+1
    dataframe['statusn2']=statusn2
    dataframe['statusn2']=dataframe['statusn2'].replace([2],[102])
    #####################################################################################################################12-27gengxin#######################################################################################
    return dataframe
                       

def trip(dataframe):
    ### 分日提取充电段
    status2=dataframe['statusn2']
    status=dataframe['current_status_vehicle']
    q_e_p=dataframe['quqantity_electricity_percent']
    time_collect=dataframe['time_collect']
    lon=dataframe['longitude']
    lat=dataframe['latitude']
    ori=dataframe['orientation']
    spe=dataframe['newspd']
    str0=pd.Series('2000-01-01 01:01:01')
    time0=str0.append(time_collect,  ignore_index=True)
    time0=time0.append(str0,  ignore_index=True)  ##头尾都加上str0
    distance_acc=dataframe['distance_accumulative']
    temp=dataframe['high_temperature']
    dis0=pd.Series([0])
    distance_acc0=dis0.append(distance_acc,ignore_index=True)
    distance_acc0=distance_acc0.append(dis0,ignore_index=True) ##头尾都加上dis0




    status2=list(status2)
    status=list(status)
    lens=len(status)
    start=[]
    stop=[]
    status20=[0]+status2+[0]
    status0=[0]+status+[0]
    k=0

    for k in range(lens):
        w1=(status20[k+1]==102 and status20[k]!=102) #如果前是move，后是stop，放入start
        w2=(status20[k+1]==102 and status20[k+2]!=102) ##如果前是stop，后是move，放入stop
        if w1:
            start.append(k)
        tt=getTimeDiff.GetTimeDiff(time0[k],time0[k+1])
        if tt>3600 and (status20[k+1]==102) and (status20[k]==102):  ##接下来的状态都是停止，
            start.append(k)
            stop.append(k-1)
        if w2:
            stop.append(k)
    
    
    if len(start)>len(stop):
        start.remove(start[-1])
    at=[]
    bt=[]
      
    for i in range(len(start)-1):###针对充电段落间隔时间过小的拼接#######################假设：如果充电段间没有里程差异，认为是一个充电段############################################################################################################
        interv=getTimeDiff.GetTimeDiff(time_collect[stop[i]],time_collect[start[i+1]])
        ##############################################################################################################12-25增加充电段拼接的附加条件:里程没有太大变化################################################################################################
        l=distance_acc[start[i+1]]-distance_acc[stop[i]]
        m=q_e_p[start[i+1]]-q_e_p[stop[i]]
        
        #if interv<15*60 and l<1:
        if  l<2 and l>-1 and m>-1 and q_e_p[start[i+1]]<100:
            at.append(i+1) #如果前后两个充电段距离短，电量没有减少，电未充满，则认为是同一个充电段
            bt.append(i)
    start=np.array(start)
    stop=np.array(stop)
    start=np.delete(start,at,axis=0)
    stop=np.delete(stop,bt,axis=0)
   
            
    start=np.array(start)
    stop=np.array(stop)
#    for i in range(start.shape[0]):
#        print(start[i],stop[i])

#    start=start.reshape(start.shape[0],1)
#    stop=stop.reshape(stop.shape[0],1)


    ## data cleaning of charging period
    # numchargedur=size(start,1);
    # startchind=[];
    # stopchind=[];
    # for i= 1:numchargedur-1
    #     %相邻后一个charge段的开头减去前一个charge段的结尾 
    #       num1=datenum(2001,01,01,12,00,00);
    #       num2=datenum(2001,01,01,12,00,01);
    #       num=num2-num1;
    #       num1=datenum(alldata.time_collect(start(i+1),:));
    #       num2=datenum(alldata.time_collect(stop(i),:));
    #       interv=(num1-num2)/num;
    #       if interv<900 %charge时间少于5分钟，删掉charge记录
    #           startchind=[startchind;i+1];
    #           stopchind=[stopchind;i];
    #       end   
    # end
    # 
    # start(startchind,:)=[];
    # stop(startchind,:)=[];
    
    
    

    # table_charge=tabulate(datestr(startchargedate));
    
    
    ### travel period
    starttrip=[]
    stoptrip=[]


    for k in range(lens):
        w1=(status0[k+1]==1 and status0[k]!=1)
        w2=(status0[k+1]==1 and status0[k+2]!=1)
        if w1:
            starttrip.append(k)
        tt=getTimeDiff.GetTimeDiff(time0[k],time0[k+1]) 
        if tt>3600 and (status0[k+1]==1) and (status0[k]==1): #and abs(distance_acc0[k+1]-distance_acc0[k])<10:
            #针对间断的时间段进行处理
            starttrip.append(k)
            stoptrip.append(k-1)
        if w2:
            stoptrip.append(k)        
    numtripdur=len(starttrip)
    startdetind=[] #需要删除的
    stopdetind=[] #需要删除的
    for i in range(numtripdur-1):
        #x=相邻后一个行程段的开头减去前一个行程段的结尾
        interv=getTimeDiff.GetTimeDiff(time_collect[stoptrip[i]],time_collect[starttrip[i+1]])
        if interv<15*60 and q_e_p[starttrip[i+1]]-q_e_p[stoptrip[i]]<=0: ##############如果停留时间少于15分钟，且中间不是充电段，删掉停留记录
            startdetind.append(i+1)
            stopdetind.append(i)
    
    starttrip=np.array(starttrip)
    stoptrip=np.array(stoptrip)
    starttrip=np.delete(starttrip,startdetind,axis=0)
    stoptrip=np.delete(stoptrip,stopdetind,axis=0)
    starttrip=starttrip.reshape(starttrip.shape[0],1)
  
    onz=np.ones((starttrip.shape[0],1))
    starttrip=np.append(onz,starttrip,axis=1)
    start=start.reshape(start.shape[0],1)



    
    onz2=np.ones((start.shape[0],1))*2
    start=np.append(onz2,start,axis=1)

    ##充电段和行程段串联
    b=np.append(starttrip,start,axis=0)
    e=np.append(stoptrip,stop,axis=0)
    re=np.zeros((b.shape[0],4))
    re[:,1:3]=b
    re[:,3]=e
    rg=np.lexsort(re.T)
    re=re[rg]

    re=re.astype(int)
    duration=np.zeros((len(re),1))
    for i in range(len(re)):
        duration[i]=getTimeDiff.GetTimeDiff(time_collect[re[i,2]],time_collect[re[i,3]])/60
    quqantity_electricity_percent=dataframe['quqantity_electricity_percent']
    q_e_p=quqantity_electricity_percent.as_matrix()
    q_e_p_begin=q_e_p[re[:,2]]
    q_e_p_begin=q_e_p_begin.reshape((len(q_e_p_begin),1))
    q_e_p_end=q_e_p[re[:,3]]
    q_e_p_end=q_e_p_end.reshape((len(q_e_p_end),1))
    longitude=dataframe['longitude']
    longitude=longitude.as_matrix()
    latitude=dataframe['latitude']
    latitude=latitude.as_matrix()
    long_begin=longitude[re[:,2]]
    long_begin=long_begin.reshape((len(long_begin),1))
    la_begin=latitude[re[:,2]]
    la_begin=la_begin.reshape((len(la_begin),1))
    long_end=longitude[re[:,3]]
    long_end=long_end.reshape((len(long_end),1))
    la_end=latitude[re[:,3]]
    la_end=la_end.reshape((len(la_end),1))
    distance_accumulative=dataframe['distance_accumulative']
    dist_cha=np.zeros((len(re),1)) 
    
    whether_weekday=np.zeros((len(re),1))  #是否工作日
    
    time_start=np.zeros((len(re),1)) 
    time_end=np.zeros((len(re),1))
    
    #dist_gap=np.zeros((len(re),1)) #计算下次段落的开始经纬度与上次段落结束的经纬度之间的距离


    #timediff=(time_endarr-time_startarr)/60 #min
    #aa=a.reshape(1,1)
    #time_startarr2=np.append(time_startarr,aa,axis=0)
    #time_startarr3=np.delete(time_startarr2,0,axis=0)
    #time_periodgap=(time_startarr3-time_endarr)/60 #min 这段结束与下段开始的差值
    a=long_begin[long_begin.shape[0]-1].reshape(1,1)
    long_begin2=np.append(long_begin,a,axis=0)
    long_begin2=np.delete(long_begin2,0,axis=0)
    a=la_begin[la_begin.shape[0]-1].reshape(1,1)
    la_begin2=np.append(la_begin,a,axis=0)
    la_begin2=np.delete(la_begin2,0,axis=0)
    
    #温度
    temperature=np.zeros((len(re),1))
    
    for i in range(len(re)):
        temperature[i]=temp[re[i,3]]
        dist_cha[i]=distance_accumulative[re[i,3]]-distance_accumulative[re[i,2]]
        whether_weekday[i]=datetime.datetime.strptime(time_collect[re[i,2]],"%Y-%m-%d %H:%M:%S").weekday()+1 #星期
        time_start[i]=float(time_collect[re[i,2]][11:13])+float(time_collect[re[i,2]][14:16])/60
        time_end[i]=float(time_collect[re[i,3]][11:13])+float(time_collect[re[i,3]][14:16])/60
        #dist_gap[i]=latlon.haversine(long_end[i,0]/1000000,la_end[i,0]/1000000,long_begin2[i,0]/1000000,la_begin2[i,0]/1000000)
    ddata=np.hstack((re,duration,q_e_p_begin,q_e_p_end,long_begin,la_begin,long_end,la_end,dist_cha,whether_weekday,time_start,time_end,temperature))
    aa=re_idx(dataframe,ddata).reshape(ddata.shape[0],)
    ddata[:,0]=aa
    ddata=ddata[ddata[:,4]>0] #把持续时间为0的事件删除
    return ddata
