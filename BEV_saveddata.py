# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 13:02:30 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 06:36:25 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import time
import os
import dvmt  #每日行程距离
import getTimeDiff
import commute   #找到家、工作地位置
import indicate123  #标识家庭和工作地住址的性质
import ChargeInroute  #途中充电
import statistic

tvmt=np.zeros((600,13))#############################################################################
## 最小值 20分位数 50分位数 75分位数 最大值 除0之后的最大值
statis_tab=np.zeros((600,35))
statis_driving_period_tab=pd.DataFrame([])
statis_driving_day_tab=pd.DataFrame([])
statis_charging_period_tab=pd.DataFrame([])
statis_charging_day_tab=pd.DataFrame([])

ddata_tab=pd.DataFrame([])

#path1=r'D:/1/1/1/chun/' 师姐
path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/bev16/'
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

#table_1=np.zeros((103,104))
time_start=time.time()
names=locals()
st=np.ones((0,13))

for i in range (1,len(file_list)):
    filename1='/Users/apple/Desktop/shakalaka/research_on_EV/data/ddatac/bev/ddatac'+str(i)+'.csv'
    filename2='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/bev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/shakalaka/research_on_EV/data/bev/ddatac'
#    filename1='D:/1/bevdata2/ddatac'+str(i)+'.csv'
#    filename2='D:/1/bevdata2/datareinx'+str(i)+'.csv'
#    path='D:/1/bevd2ata'
    if os.path.exists(filename1)==True:
        
        ddata=np.array(pd.read_csv(filename1))
        datareinx=pd.read_csv(filename2)
        ddata_tab=pd.concat([ddata_tab,pd.DataFrame(ddata)],axis=0,ignore_index=True)
    
    charginwper,charginhper,nw,nh,commuted,work_place,home_place=commute.commutetab(ddata,datareinx)
        
    #一些统计值
    stat_driving_period,stat_driving_day,stat_charging_period,stat_charging_day=statistic.stat(ddata,datareinx)
    statis_driving_period_tab=pd.concat([statis_driving_period_tab,pd.DataFrame(stat_driving_period)],axis=0,ignore_index=True)
    statis_driving_day_tab=pd.concat([statis_driving_day_tab,pd.DataFrame(stat_driving_day)],axis=0,ignore_index=True)
    statis_charging_period_tab=pd.concat([statis_charging_period_tab,pd.DataFrame(stat_charging_period)],axis=0,ignore_index=True)
    statis_charging_day_tab=pd.concat([statis_charging_day_tab,pd.DataFrame(stat_charging_day)],axis=0,ignore_index=True)
        
    statis=statistic.statis(ddata,datareinx)
    for k in range(0,35):
        statis_tab[i,k]=statis[k]
        
        
    tvmt[i,0],tvmt[i,1],tvmt[i,2],tvmt[i,3],tvmt[i,4],tvmt[i,5],tvmt[i,6],odov=dvmt.dvmt1(datareinx)##要对数据清洗后的数据进行处理
    
    ddata2=indicate123.indichwp(ddata,work_place,home_place)
    ddata2=ddata2[ddata2[:,4]!=0]

    
    if max(ddata2[:,-1])==123 or work_place.iloc[2]<0.2 or nw<30 or nh<30:
       # tvmt[i,7]=8888
        print('failtoidentifyhw')
        cirinx=ChargeInroute.cin(ddata2,datareinx)
        cn=np.zeros((cirinx.shape[0],13))
        cn[:,0:11]=cirinx
        cn[:,11]=0###代表非通勤
        cn[:,12]=i#代表用户编号
        cn=cn[cn[:,1]<200]
        
        cn=cn[cn[:,2]<200]
        #cn=cn[cn[:,6]<0]##充电电流不可能大于0
        cn=cn[cn[:,1]>0]
        cn=cn[cn[:,2]>0]
    
        
        
        g=ddata2[ddata2[:,1]==2] #所有充电事件
        g1=g[g[:,-1]==123]
        tvmt[i,8]=ddata2[ddata2[:,1]==2].shape[0]##所有充电事件的个数8
        tvmt[i,9]=g1.shape[0]#家充事件总数9
        tvmt[i,10]=cn.shape[0]#途中充电总数10
        tvmt[i,12]=int(getTimeDiff.GetTimeDiff(datareinx['time_collect'].iloc[0],datareinx['time_collect'].iloc[-1])/(60*60*24))#记录时间12
    
    else:
        tvmt[i,7]=dvmt.commutea(ddata2,datareinx)##计算通勤距离
        cirinx=ChargeInroute.cin(ddata2,datareinx)
        cn=np.zeros((cirinx.shape[0],13))
        cn[:,0:11]=cirinx
        cn[:,11]=1###代表通勤
        cn[:,12]=i#代表用户编号
        cn=cn[cn[:,1]<200]
        cn=cn[cn[:,2]<200]
        #cn=cn[cn[:,6]<0]##充电电流不可能大于0
        cn=cn[cn[:,1]>0]
        cn=cn[cn[:,2]>0]
        g=ddata2[ddata2[:,1]==2] #所有充电事件
        g1=g[g[:,-1]==100]
        g2=g[g[:,-1]==30]
        tvmt[i,8]=ddata2[ddata2[:,1]==2].shape[0]##所有充电事件的个数
        tvmt[i,9]=g1.shape[0]#家充事件总数
        tvmt[i,10]=cn.shape[0]#途中充电总数
        tvmt[i,11]=g2.shape[0]#工作地充电总数
        tvmt[i,12]=int(getTimeDiff.GetTimeDiff(datareinx['time_collect'].iloc[0],datareinx['time_collect'].iloc[-1])/(60*60*24))#记录时间
    

    ncn=np.zeros(((st.shape[0]+cn.shape[0]),13))
    ncn[:st.shape[0],:]=st
    if cn.shape[0]==0:
        st=ncn
    else:
        ncn[(-cn.shape[0]):,:]=cn
        st=ncn
            

    print(i)
    print(time.time()-time_start)
    
    
    
    
####保存数据
def savedd(data,fstr):
    aa=pd.DataFrame(data)
    name='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/store/bev_'+fstr+'.csv'
    aa.to_csv(name,index=False)
    
savedd(tvmt,'tvmt')
savedd(statis_tab,'statis_tab')
savedd(statis_driving_period_tab,'statis_driving_period_tab')
savedd(statis_driving_day_tab,'statis_driving_day_tab')
savedd(statis_charging_period_tab,'statis_charging_period_tab')
savedd(statis_charging_period_tab,'statis_charging_period_tab')

savedd(ddata_tab,'ddata_tab')