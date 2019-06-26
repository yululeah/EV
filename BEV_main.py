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

import data_processing
import numpy as np
import time
import os
import transn
import dvmt
import getTimeDiff
import commute
import indicate123
import ChargeInroute


tvmt=np.zeros((600,13))#############################################################################
## 最小值 20分位数 50分位数 75分位数 最大值 除0之后的最大值

#path1=r'D:/1/1/1/chun/'
path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/bev16/'
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

#table_1=np.zeros((103,104))
time_start=time.time()
names=locals()
st=np.ones((0,13))

for i in range(1,len(file_list)):
        
    fp=path1+file_list[i]

    df=data_processing.loadData3(fp)
    ddata,datareinx=transn.datac(df)

    charginwper,charginhper,nw,nh,commuted,work_place,home_place=commute.commutetab(ddata,datareinx)

    tvmt[i,0],tvmt[i,1],tvmt[i,2],tvmt[i,3],tvmt[i,4],tvmt[i,5],tvmt[i,6],odov=dvmt.dvmt1(datareinx)##要对数据清洗后的数据进行处理

    ddata2=indicate123.indichwp(ddata,work_place,home_place)

    
    if max(ddata2[:,-1])==123 or work_place.iloc[2]<0.2 or nw<30 or nh<30:
       # tvmt[i,7]=8888
        print('failtoidentifyhw')
        cirinx=ChargeInroute.cin(ddata2,datareinx)
        cn=np.zeros((cirinx.shape[0],13))
        cn[:,0:11]=cirinx
        cn[:,11]=0###代表飞通勤
        cn[:,12]=i#代表用户编号
        cn=cn[cn[:,1]<200]
        
        cn=cn[cn[:,2]<200]
        #cn=cn[cn[:,6]<0]##充电电流不可能大于0
        cn=cn[cn[:,1]>0]
        cn=cn[cn[:,2]>0]
       
        
        g=ddata2[ddata[:,1]==2] #所有充电事件
        g1=g[g[:,-1]==123]
        tvmt[i,8]=ddata2[ddata[:,1]==2].shape[0]##所有充电事件的个数8
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
        g=ddata2[ddata[:,1]==2] #所有充电事件
        g1=g[g[:,12]==100]
        g2=g[g[:,12]==30]
        tvmt[i,8]=ddata2[ddata[:,1]==2].shape[0]##所有充电事件的个数
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
