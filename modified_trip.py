import data_analysis
import getTimeDiff
import datetime
import numpy as np
import pandas as pd

def trip(dataframe):

#    dataframe=datareinx_temp
    ### 分日提取充电段
    status2=dataframe['statusn2']
    status=dataframe['current_status_vehicle']
    q_e_p=dataframe['quqantity_electricity_percent']
    time_collect=dataframe['time_collect']
    str0=pd.Series('2000-01-01 01:01:01')
    time0=str0.append(time_collect,  ignore_index=True)  #重新赋值index
    time0=time0.append(str0,  ignore_index=True)  ##头尾都加上str0
    distance_acc=dataframe['distance_accumulative']
#    fuel_acc=dataframe['fuel_accumulate']
#    dis0=pd.Series([0])
#    distance_acc0=dis0.append(distance_acc,ignore_index=True) #重新赋值index
#    distance_acc0=distance_acc0.append(dis0,ignore_index=True) ##头尾都加上dis0
#    fuel0=pd.Series([0])
#    fuel_acc0=fuel0.append(fuel_acc,ignore_index=True)
#    fuel_acc0=fuel_acc0.append(fuel0,ignore_index=True) ##头尾都加上fuel0




    status2=list(status2)
    status=list(status)
    lens=len(status) #记录数
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
        interv=getTimeDiff.GetTimeDiff(time_collect[stop[i]+dataframe.iat[0,0]],time_collect[start[i+1]+dataframe.iat[0,0]])
        ##############################################################################################################12-25增加充电段拼接的附加条件:里程没有太大变化################################################################################################
        l=distance_acc[start[i+1]+dataframe.iat[0,0]]-distance_acc[stop[i]+dataframe.iat[0,0]]
        m=q_e_p[start[i+1]+dataframe.iat[0,0]]-q_e_p[stop[i]+dataframe.iat[0,0]]
        
        #if interv<15*60 and l<1:
        if  l<2 and l>-1 and m>-1 and q_e_p[start[i+1]+dataframe.iat[0,0]]<100:
            at.append(i+1) #如果前后两个充电段距离短，电量没有减少，电未充满，则认为是同一个充电段
            bt.append(i)
    start=np.array(start)
    stop=np.array(stop)
    start=np.delete(start,at,axis=0)
    stop=np.delete(stop,bt,axis=0)
   
            
    start=np.array(start)
    stop=np.array(stop)
    
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
        interv=getTimeDiff.GetTimeDiff(time_collect[stoptrip[i]+dataframe.iat[0,0]],time_collect[starttrip[i+1]+dataframe.iat[0,0]])
        if interv<15*60 and q_e_p[starttrip[i+1]+dataframe.iat[0,0]]-q_e_p[stoptrip[i]+dataframe.iat[0,0]]<=0: ##############如果停留时间少于15分钟，且中间不是充电段，删掉停留记录
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
    re[:,1:3]=b #天数，状态，starttrip
    re[:,3]=e #stoptrip
    rg=np.lexsort(re.T)
    re=re[rg]

    re=re.astype(int)
    
    if len(re)>0:
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
        
        fuel_accumulative=dataframe['fuel_accumulate']
        dist_cha=np.zeros((len(re),1)) 
        fuel_cha=np.zeros((len(re),1)) 
        whether_weekday=np.zeros((len(re),1))  #是否工作日
        
        time_start=np.zeros((len(re),1)) 
        time_end=np.zeros((len(re),1))
        
        
        duration=np.zeros((len(re),1))        
        for i in range(len(re)):
            re[i,2]=dataframe.iat[re[i,2],0] 
            re[i,3]=dataframe.iat[re[i,3],0] 
            duration[i]=getTimeDiff.GetTimeDiff(time_collect[re[i,2]],time_collect[re[i,3]])/60
            
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
        
        
        for i in range(len(re)):
            dist_cha[i]=distance_acc[re[i,3]]-distance_acc[re[i,2]]
            fuel_cha[i]=fuel_accumulative[re[i,3]]-fuel_accumulative[re[i,2]]
            whether_weekday[i]=datetime.datetime.strptime(time_collect[re[i,2]],"%Y-%m-%d %H:%M:%S").weekday()+1 #星期
            time_start[i]=float(time_collect[re[i,2]][11:13])+float(time_collect[re[i,2]][14:16])/60
            time_end[i]=float(time_collect[re[i,3]][11:13])+float(time_collect[re[i,3]][14:16])/60
            #dist_gap[i]=latlon.haversine(long_end[i,0]/1000000,la_end[i,0]/1000000,long_begin2[i,0]/1000000,la_begin2[i,0]/1000000)
        dddata=np.hstack((re,duration,q_e_p_begin,q_e_p_end,long_begin,la_begin,long_end,la_end,dist_cha,whether_weekday,time_start,time_end,fuel_cha))
    #    aa=data_analysis.re_idx(dataframe,ddata).reshape(ddata.shape[0],)
    #    ddata[:,0]=aa
    #    ddata=ddata[ddata[:,4]>0] #把持续时间为0的事件删除
    
    else:
        dddata=np.zeros((1,16))-1
        
    return dddata
