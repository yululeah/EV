# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:26:16 2018

@author: anita
"
"""

import numpy as np
import statsmodels.api as sm
import consumptionana
from sklearn.metrics import r2_score
######相关性分析





def fresult(ddata,datareinx):
    dg=consumptionana.ct3(ddata,datareinx)
    if len(dg[0])>0:
#        cf=np.array(dg[0])
        cf=np.array(dg[3]) ##这里区分是用电量还是能量（有一些可能电能量缺失，或者电量显示有问题，需要修正之类的） ##soc变化
        ce=np.array(dg[1])/1000 #使用的燃油量
        cff=np.array(dg[0]) 
        pdf=sum(cff)*0.67/(sum(cff)*0.67+sum(ce)*0.179*8.9)
        cf=cf.reshape(len(cf),1)
        ce=ce.reshape(ce.shape[0],1)
        tcc=np.array(dg[4]) #耗时
        XX=np.hstack((cf,ce))  #拼接数组的方法：np.vstack():在竖直方向上堆叠 np.hstack():在水平方向上平铺
        Y=np.array(dg[2]).reshape(cf.shape[0],)  #里程
        
    ######输出相关矩阵的第一列
    
    #######筛选后的数据读取
    
    ######筛选后的变量######
        X1 = XX
        #X1=sm.add_constant(X1)
        Y1 = Y
        r_i=X1[:,1]<50 #使用的燃油量小于50
        X1=X1[r_i,:]
        Y1=Y1[r_i]
        
        r_i=X1[:,1]>=0  #使用的燃油量大于0
        X1=X1[r_i,:]
        Y1=Y1[r_i]
        r_i=X1[:,0]<100 ##soc小于100
        X1=X1[r_i,:]
        Y1=Y1[r_i]
        r_i=X1[:,0]>-100 ##soc大于-100
        X1=X1[r_i,:]
        Y1=Y1[r_i]
        
        if len(X1[X1[:,1]!=0])==0:  #如果纯用电
            est=sm.OLS(Y1,X1[:,0]).fit()
            tv=est.tvalues
            pare=est.params
            per1=1 #电里程比例
            per2=1
            t1=tv[0]
            t2=0
            p1=pare[0]
            p2=0
            
        
        else: #既用油又用电
            
        
            est = sm.OLS(Y1,X1).fit()
            tv=est.tvalues
            pare=est.params
    #        print(est.summary())
            
            ya=sum(Y1)
            pv=pare[1]*sum(ce) #fuel
            ev=pare[0]*sum(cf) #soc
            per1=ev/ya #电里程比例
            per2=1-pv/ya #电里程比例
            t1=tv[0]
            t2=tv[1]
            p1=pare[0]
            p2=pare[1]
        
        
        
    #print(est.summary())
        return t1,t2,p1,p2,per1,per2,X1,Y1,sum(ce),sum(Y),pdf
    
    else:
        return None


#j1=np.zeros((26,6))
#import cleanfuel
#for i in range(1,8):
##    d0=eval('dd'+str(i))[0]
##    d1=eval('dd'+str(i))[1]
#    d0,d1=trans.datac(eval('ddata_'+str(i)))
#    dd=cleanfuel.task3(d1,d0)
#    ddata=d1
#    print(i,len(d0)-len(dd))
#    #ddata=eval('ddata_'+str(i))
#    if len(dd[dd[:,1]==1])==0:
#        continue
#    else:
#        aa=fresult(dd,d1)
#        j1[i,0]=aa[0]
#        j1[i,1]=aa[1]
#        j1[i,2]=aa[2]
#        j1[i,3]=aa[3]
#        j1[i,4]=aa[4]
#        j1[i,5]=aa[5]
def frec(ddata,datareinx):
    dg=consumptionana.ct(ddata,datareinx)
    cf=np.array(dg[3]) ##这里区分是用电量还是能量（有一些可能电能量缺失，或者电量显示有问题，需要修正之类的）
    ce=np.array(dg[1])/1000
    cf=cf.reshape(len(cf),1)
    ce=ce.reshape(ce.shape[0],1)
    XX=np.hstack((cf,ce))
    Y=np.array(dg[2]).reshape(cf.shape[0],)

######输出相关矩阵的第一列

#######筛选后的数据读取

######筛选后的变量######
    X1 = XX
    #X1=sm.add_constant(X1)
    Y1 = Y
    r_i=X1[:,1]<50
    X1=X1[r_i,:]
    Y1=Y1[r_i]
    
    r_i=X1[:,1]>=0
    X1=X1[r_i,:]
    Y1=Y1[r_i]
    r_i=X1[:,0]<100
    X1=X1[r_i,:]
    Y1=Y1[r_i]
    r_i=X1[:,0]>-100
    X1=X1[r_i,:]
    Y1=Y1[r_i]
    
    if len(X1[X1[:,1]!=0])==0:
        #est=sm.OLS(Y1,X1[:,0]).fit()
        per1=1
        per2=1
  
    
    
    
#        est = sm.OLS(Y1,X1).fit()
#        tv=est.tvalues
#        pare=est.params
    
        #ya=sum(Y)
#        pv=pare[1]*sum(ce)
#        ev=pare[0]*sum(cf)
#        per1=ev/ya
#        per2=1-pv/ya
#        t1=tv[0]
#        t2=tv[1]
#        p1=pare[0]
#        p2=pare[1]
        
        
        
    #print(est.summary())
    return sum(X1[:,0]),sum(Y1)



def olsa_5min(dg):
#    dg=data_olas
    ##每个行程切成5分钟，做出系数
    if len(dg)>0:
        cf=np.array(dg[:,2]) ##电
        ce=np.array(dg[:,4])*8.9/1000#使用的燃油量
        cf=cf.reshape(len(cf),1)
        ce=ce.reshape(ce.shape[0],1)
        XX=np.hstack((cf,ce))  #拼接数组的方法：np.vstack():在竖直方向上堆叠 np.hstack():在水平方向上平铺
        Y=np.array(dg[:,1]).reshape(cf.shape[0],)  #里程
        

        #时间
        t=sum(dg[:,0])/3600
        #里程
        vmt=sum(dg[:,1])
        ######输出相关矩阵的第一列
        
        #######筛选后的数据读取
        
        ######筛选后的变量######
        X1 = XX
#            #X1=sm.add_constant(X1)
        Y1 = Y
#            r_i=X1[:,1]<50 #使用的燃油量小于50
#            X1=X1[r_i,:]
#            Y1=Y1[r_i]
#            
#            r_i=X1[:,1]>=0  #使用的燃油量大于0
#            X1=X1[r_i,:]
#            Y1=Y1[r_i]
#            r_i=X1[:,0]<100 ##soc小于100
#            X1=X1[r_i,:]
#            Y1=Y1[r_i]
#            r_i=X1[:,0]>-100 ##soc大于-100
#            X1=X1[r_i,:]
#            Y1=Y1[r_i]
            
#            if len(X1[X1[:,1]!=0])==0:  #如果纯用电
#                est=sm.OLS(Y1,X1[:,0]).fit()
#                tv=est.tvalues
#                pare=est.params
#                per1=1 #电里程比例
#                per2=1
#                t1=tv[0]
#                t2=0
#                p1=pare[0]
#                p2=0
#                
#            
#            else: #既用油又用电
                
            
        est = sm.OLS(Y1,X1).fit()
        tv=est.tvalues
        pare=est.params
#        print(est.summary())
        
        ya=sum(Y1)
        ev=pare[0]*sum(cf) #elec_energy
        pv=pare[1]*sum(ce) #fuel
        per1=ev/ya #电里程比例
        per2=1-pv/ya #电里程比例
        t1=tv[0]
        t2=tv[1]
        p1=pare[0]
        p2=pare[1]
        
        Real_Values=Y
        Predict_Values=np.dot(X1,np.transpose([p1,p2]))
        

        r2 = r2_score(Real_Values , Predict_Values )
        #print(est.summary())
        return p1,p2,ev,pv,t,vmt,r2
    else:
        return None