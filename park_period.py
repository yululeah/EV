# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:10:57 2018

@author: anita
"""
#import numpy as np
#import pandas as pd
#import trans

def dwell(dada):
    import numpy as np
    import pandas as pd
#    import trans
#    import datetime

    d_c=dada['distance_accumulative']
#    t_s=trans.timest(dada)
#
#    trp=pd.concat([t_s,d_c],axis=1)
    
    ds=dada['distance_accumulative'].shift(-1)
    dsmda=ds-dada['distance_accumulative']
    t_c=dada['time_collect']
    t_cg=pd.to_datetime(t_c)
    t_ct=t_cg.reset_index(drop=True)
    dsmdaa=np.array(dsmda)
    st=np.zeros((dsmdaa.shape[0],))
    i=0
    while i<dsmdaa.shape[0]-1:
        if dsmdaa[i]==0:
            j=i
            while dsmdaa[j]==0:
                j=j+1
            trpa=t_ct[j]-t_ct[i]
            if trpa.total_seconds()>15*60:# and abs(soca[i]-soca[j])<10 :##设置停留时间大于15分钟则作为停留段落
                st[i:j]=188
                i=j
        
        i=i+1
    st=pd.Series(st, index=list(t_cg.index))
    stc=st[st!=0]
    dwellinx=list(stc.index)
    return dwellinx




def pp2(data):
    import pandas as pd
#    import trans
    import getTimeDiff
#    import datetime
#    import l_s
#    import latlon
    #data=trans.datacleaning(data)
    statusn=data['current_status_vehicle']
    q_e_p=data['quqantity_electricity_percent']
    odom=data['distance_accumulative']
    t_c=data['time_collect']
    lon=data['longitude']
    lat=data['latitude']
    #dwellinx=dwell(data)
    #statusn[dwellinx]=0
    #data['current_vehicle_status']=statusn

    

   
    i=0
    start=[]
    stop=[]
    ps=[]
    pe=[]
    hs=[]
    he=[]
    #ixlist=list(statusn.index)
    
#    while i<len(ixlist)-1:
#        if i==0 and ixlist[0]==0 and statusn[ixlist[0]]==101:
#            start.append(i)
#        if statusn[ixlist[i]]!=101 and statusn[ixlist[i+1]]==101:
#            start.append(ixlist[i+1])
#        if statusn[ixlist[i]]==101 and statusn[ixlist[i+1]]!=101:
#            stop.append(ixlist[i])
#        if i==endin and statusn[endin]==101:
#            stop.append(endin)
#        i=i+1
        
    while i<len(statusn)-2:
        if i==0 and  statusn[0]==0: #第一个状态
            start.append(i)
            j=i+1
            while odom[j]==odom[i] and j<len(statusn)-1:  #当里程没有增加，则j+1
                j=j+1
            stop.append(j-1) #当里程增加时，stop有了索引
            

            i=j-1
            
        if i>0 and statusn[i]==0 and statusn[i+1]==0 and getTimeDiff.GetTimeDiff(t_c[i-1],t_c[i])<=20*60:
            start.append(i)
            j=i+1
            while odom[j]==odom[i+1] and j<len(statusn)-1:
                j=j+1
            stop.append(j-1)

            i=j-1

        #if i==endin-1 and statusn[endin-1]==0:
           # stop.append(endin-1)
            
        if statusn[i]!=0 and odom[i+1]-odom[i]< 2 and getTimeDiff.GetTimeDiff(t_c[i],t_c[i+1])>20*60:  
         ##如果状态不为0，下一个状态-上一个状态里程小于2，时间间隔大于20min
            start.append(i)
            j=i+1
            while odom[i]==odom[j] and j<len(statusn)-1:
                j=j+1
            stop.append(j)

            i=j
        
        i=i+1
    while(len(start)!=len(stop)):
        if len(start)>len(stop):
            del(start[-1])
        else:
            del(stop[-1])
        
 
    
#
    for i in range(len(start)):

  
        t1hour=pd.Timestamp(t_c[start[i]]).hour
        #print(i,start[i],stop[i])
        t2hour=pd.Timestamp(t_c[stop[i]]).hour
 
        
        xq1=pd.Timestamp(t_c[start[i]]).weekday()
        xq2=pd.Timestamp(t_c[start[i]]).weekday()
        if getTimeDiff.GetTimeDiff(t_c[start[i]],t_c[stop[i]])>2*60*60 and t1hour>4 and t2hour<22  and t1hour<17  and t1hour<t2hour\
        and getTimeDiff.GetTimeDiff(t_c[start[i]],t_c[stop[i]])<12*60*60\
        and xq1<6 and xq2<6 and xq1>0 and xq2>0:##保证在工作日  而且是白天  间隔不短于2h，不超过12h
            ps.append(start[i])
            pe.append(stop[i])
            k=q_e_p[stop[i]]-q_e_p[start[i]]

            #print(start[i],stop[i])
            #print(1,startstop[i]],lon[start[i]],lat[start[i]],xq1)
        
        if getTimeDiff.GetTimeDiff(t_c[start[i]],t_c[stop[i]])>2*60*60 and (t1hour>16 or t1hour<5): #在夜晚
            hs.append(start[i])
            he.append(stop[i])
            k=q_e_p[stop[i]]-q_e_p[start[i]]
            #print(start[i],stop[i]) ##########################
            

    #lon1,lon2=lon[ps],lon[pe].reset_index(drop=True)
    #lat1,lat2=lat[ps],lat[pe].reset_index(drop=True)
    #lonh1,lath1=lon[hs],lat[hs]

    
    
    
    
    lonlatds=pd.concat([lon[ps],lat[ps]],axis=1)
    lonlaths=pd.concat([lon[hs],lat[hs]],axis=1)
    
    
    return lonlatds,lonlaths
#    
#            
#            


