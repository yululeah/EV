#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 16:15:38 2019
工作模式辨别 
PHEV 在各数据段是处于纯电动模式、混合
驱动模式、内燃机模式和行车充电模式中的哪一种。
@author: apple
"""
import numpy as np
import getTimeDiff
import olsan


def mode(ddata,datareinx):
    qe=datareinx['quqantity_electricity']
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']
    
    ddm10=ddata[ddata[:,1]==1] #行程段
    
    total_vmt=sum(ddm10[:,11])
    
    data_divert_T=np.zeros((1,5))
    
    p=np.zeros((1,2))
        
        
    T=8 #时间间隔
    Ehybrid=[]
    Qhybeid=[]
    Qengine1=[]
    Qengine2=[]
    Epure=[]
    
    vmt_hybrid=0
    vmt_engine1=0
    vmt_engine2=0
    vmt_pure=0
    for i in range (ddm10.shape[0]):
        a=int(ddm10[i,2]) #索引
        b=int(ddm10[i,3]) #索引
        
        
        data_olas=np.zeros((1,5))
                
        fcc=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
        fce=qep.loc[a]-qep.loc[b] #soc
        vmt=da.loc[b]-da.loc[a] #距离
        tccc=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b]) # 时间
        
        daa=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
        dau=da.loc[a:b-1].reset_index(drop=True) 
        fcb=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
        fca=sum((daa-dau)*fcb/1000) # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量
        

        '''判断是不是烧油的行程段'''
        if any(fc.loc[a+1:b]>500):  #大于500就是在烧油驱动
            
            if fce>0:  #混合驱动
                Ehybrid.append(fcc/vmt*100)
                Qhybeid.append(fca/vmt)
                vmt_hybrid+=vmt
# =============================================================================
#                 

#                k=a
#                #                for k in range((index_start,index_end)):
#                while k<b:
#                    time_start=datareinx['time_collect'].loc[k]
#                    da_start=datareinx['distance_accumulative'].loc[k]
#                    qe_start=datareinx['quqantity_electricity'].loc[k]
#                    qep_start=datareinx['quqantity_electricity_percent'].loc[k]
#    #                fa_start=datareinx_temp['fuel_accumulate'].loc[k]
#                
#                    while getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k])<T*60 and k<b :#如果在5分钟内
#                        k=k+1
#                #break出来的时候，就是找到了那个大于5分钟的值？
#                
#                    daaa=da.loc[a+1:k-1].reset_index(drop=True) #distance_accumulative
#                    dauu=da.loc[a:k-2].reset_index(drop=True) 
#                    fcbb=fc.loc[a+1:k-1].reset_index(drop=True) #fuel_consumption
#                #持续时间、路程、soc变化、燃油变化
#                    data_divert_T_temp=np.hstack((getTimeDiff.GetTimeDiff(time_start,datareinx['time_collect'].loc[k-1]), \
#                                              datareinx['distance_accumulative'].loc[k-1]-da_start, \
#                                              qe_start-datareinx['quqantity_electricity'].loc[k-1], \
#                                              (qep_start+datareinx['quqantity_electricity_percent'].loc[k-1])/2, \
#                                              sum((daaa-dauu)*fcbb/100)))   ##油耗
#                    data_olas=np.vstack((data_olas,data_divert_T_temp))
#                
#        
#                
#                    data_divert_T=np.vstack((data_divert_T,data_divert_T_temp))
                    
                    
# =============================================================================
                    
            elif fce==0:    #内燃机
                Qengine1.append(fca/vmt)
                vmt_engine1+=vmt
            elif fce<0 and tccc>120:  #行车充电
                Qengine2.append(fca/vmt)
                vmt_engine2+=vmt
                
        else:  #纯电动模式
            Epure.append(fcc/vmt*100)
            vmt_pure+=vmt
            
        
        

        
        
        
        
        
        
        
        
        
        
        
        
# =============================================================================
#         
#
#        
#        data_olas=np.delete(data_olas,0,axis=0)
#        data_olas=np.delete(data_olas,np.where(data_olas[:,1]==0),axis=0)
#        ##做olsa
#        if len(data_olas)>3:
#            p1,p2,ev,pv,t,vmt,r2=olsan.olsa_5min(data_olas)
#            if r2>0.7:
##                data_divert=np.vstack((data_divert,[float(ev),float(pv),t,vmt]))
#                p=np.vstack((p,[p1,p2]))
#            
#    para1=np.mean(p[:,0])
#    para2=np.mean(p[:,1])
#    data_divert_T=np.delete(data_divert_T,np.where(data_divert_T[:,1]==0),axis=0)
#
#    return data_divert_T,para2/para1
#    
# ============================================================================= 
    # 计算样本 PHEV 的纯电动行驶平均百公里电耗
    Epure=np.array(Epure)
    Epure=np.delete(Epure,np.where(Epure[:]<0))
    Epure=np.mean(Epure)  
    
    
    return Epure,vmt_hybrid/total_vmt
    
    
    
    
    
    
    
    
    
    