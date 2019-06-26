# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 06:36:25 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import time
import os
import cleanfuel
import olsan
import modified_consumptionana

def modified_olsa(ddata_fuel):
    import statsmodels.api as sm
    ddm10=ddata_fuel[ddata_fuel[:,1]==1] #行程段
    change_soc=ddm10[:,5]-ddm10[:,6]  #soc变化
    change_fuel=ddm10[:,15]/1000 #fuel
    change_vmt=ddm10[:,11] #里程
    
    X1 = np.vstack((change_soc,change_fuel))
    X1 = np.transpose(X1)
    Y1 = change_vmt
    
    est = sm.OLS(Y1,X1).fit()
    tv=est.tvalues
    pare=est.params
#   print(est.summary())
    
    ya=sum(Y1)
    pv=pare[1]*sum(change_fuel) #fuel
    ev=pare[0]*sum(change_soc) #soc
    per1=ev/ya #电里程比例
    per2=1-pv/ya #电里程比例
    t1=tv[0]
    t2=tv[1]
    p1=pare[0]
    p2=pare[1]
    
    from sklearn.linear_model import LinearRegression
    l=LinearRegression()
    l.fit(X1,Y1)
    l.score(X1,Y1)
     
        
    return t1,t2,p1,p2,per1,per2,X1,Y1,sum(change_fuel),sum(Y1),l.score(X1,Y1)



# =============================================================================
# 
# =============================================================================

path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/hybrid16/'
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

data_fuel_tab=np.zeros((1,16))
data_divert_T_tab=np.zeros((1,4))


j1=np.zeros((600,8))##记录能耗的各项参数
time_start=time.time()

for i in range (1,len(file_list)):
    filename1='/Users/apple/Desktop/shakalaka/research_on_EV/data/ddatac/phev/ddatac'+str(i)+'.csv'
    filename2='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/phev/datareinx'+str(i)+'.csv'
    path='/Users/apple/Desktop/shakalaka/research_on_EV/data/phev/ddatac'
#    filename1='D:/1/72282/ddata2c'+str(i)+'.csv'
#    filename2='D:1/72282/datareinx'+str(i)+'.csv'
#    path='D:/1/72282'
    if os.path.exists(filename1)==True:
        
        ddata=np.array(pd.read_csv(filename1))
        datareinx=pd.read_csv(filename2)

        #新增的
        ddata_fuel,data_divert_T=modified_consumptionana.modified_ct(ddata,datareinx)
        data_fuel_tab=np.vstack((data_fuel_tab,ddata_fuel))
        data_divert_T_tab=np.vstack((data_divert_T_tab,data_divert_T))
    
#        ddata=cleanfuel.task3(ddata_fuel,ddata) #清洗


        if len(ddata_fuel)==0:
            continue
        else:
            aa=modified_olsa(ddata_fuel)
#            aa=olsan.fresult(ddata,datareinx)
            j1[i,0]=aa[0]###soc的t值
            j1[i,1]=aa[1]###耗油量的t值
            j1[i,2]=aa[2]###soc的coef
            j1[i,3]=aa[3]##
            j1[i,4]=aa[4]###电里程比例1
            j1[i,5]=aa[5]###电里程比例2
            j1[i,6]=aa[10] #r方
            #j1[i,6]=aa[2]*aa[8]/aa[9]
            #sce,sy=olsan.frec(data,datareinx)
            #cper=sce*aa[2]/sy
            #j1[i,6]=cper

            
     
    print(i)
    print(time.time()-time_start)
    
data_fuel_tab=np.delete(data_fuel_tab,0,axis = 0) #删去第一行  
    
def savedd(data,fstr):
    aa=pd.DataFrame(data)
    name='/Users/apple/Desktop/shakalaka/电动车行为研究/数据/store/phev_'+fstr+'.csv'
    aa.to_csv(name,index=False)
    
savedd(j1,'olsa_result')


