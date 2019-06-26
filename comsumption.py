#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:17:49 2019
计算每t分钟的油耗、电耗、soc等
@author: apple
"""

def ct(ddata,datareinx):
    import numpy as np
    import getTimeDiff
    import olsan
    qe=datareinx['quqantity_electricity']
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']

    ddm10=ddata[ddata[:,1]==1] #行程段
    
    data_divert=np.zeros((1,4))
    data_divert_T=np.zeros((1,5))
    T=8 #时间间隔
#    p1=[]
#    p2=[]
    p=np.zeros((1,2))
    
    for i in range (ddm10.shape[0]):
        a=int(ddm10[i,2]) #索引
        b=int(ddm10[i,3]) #索引
        
        
        data_olas=np.zeros((1,5))
        
        
        '''判断是不是烧油的行程段'''
        
#        ddd_temp=datareinx.loc[a:b]
        if any(fc.loc[a+1:b]>500):  #大于500就是在烧油驱动
        
            fcc=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
            fce=qep.loc[a]-qep.loc[b] #soc
            tccc=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b])/3600 #换算成小时
            daa=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
            dau=da.loc[a:b-1].reset_index(drop=True) 
            fcb=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
            fca=sum((daa-dau)*fcb/100) # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量
#    
#            aa=(daa-dau)*fcb/100
# =============================================================================
            k=a
            #                for k in range((index_start,index_end)):
            while k<b:
                time_start=datareinx['time_collect'].loc[k]
                da_start=datareinx['distance_accumulative'].loc[k]
                qe_start=datareinx['quqantity_electricity'].loc[k]
                qep_start=datareinx['quqantity_electricity_percent'].loc[k]
#                fa_start=datareinx_temp['fuel_accumulate'].loc[k]
            
                while getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k])<T*60 and k<b :#如果在5分钟内
                    k=k+1
            #break出来的时候，就是找到了那个大于5分钟的值？
            
                daaa=da.loc[a+1:k-1].reset_index(drop=True) #distance_accumulative
                dauu=da.loc[a:k-2].reset_index(drop=True) 
                fcbb=fc.loc[a+1:k-1].reset_index(drop=True) #fuel_consumption
            #持续时间、路程、soc变化、燃油变化
                data_divert_T_temp=np.hstack((getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k-1]), \
                                          datareinx['distance_accumulative'].loc[k-1]-da_start, \
                                          qe_start-datareinx['quqantity_electricity'].loc[k-1], \
                                          (qep_start+datareinx['quqantity_electricity_percent'].loc[k-1])/2, \
                                          sum((daaa-dauu)*fcbb/100)))   ##油耗
                data_olas=np.vstack((data_olas,data_divert_T_temp))
                
        
                
                data_divert_T=np.vstack((data_divert_T,data_divert_T_temp))
                
        data_olas=np.delete(data_olas,0,axis=0)
        data_olas=np.delete(data_olas,np.where(data_olas[:,1]==0),axis=0)
        ##做olsa
        if len(data_olas)>3:
            p1,p2,ev,pv,t,vmt,r2=olsan.olsa_5min(data_olas)
            if r2>0.7:
                data_divert=np.vstack((data_divert,[float(ev),float(pv),t,vmt]))
                p=np.vstack((p,[p1,p2]))
    # =============================================================================
    para1=np.mean(p[:,0])
    para2=np.mean(p[:,1])
            
    data_divert_T=np.delete(data_divert_T,0,axis=0)
    data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,1]==0),axis=0)
    data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,1]==0),axis=0)
    para1,para2,Ev,Pv,T,Vmt,rsquare2=olsan.olsa_5min(data_divert_T)
    
    return data_divert_T,para2/para1
    #耗时, 里程，电池能量，soc，燃油量
#
    dg=np.vstack((np.array(cf),np.array(ce),np.array(cd),np.array(cs),np.array(tcc)))
    dg=np.transpose(dg)
    np.sum(np.array(cf))


##每一个行程拟合一个方程
