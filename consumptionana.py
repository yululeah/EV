# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 21:41:14 2018

@author: anita
"""

def ct(ddata,datareinx):
    import getTimeDiff
    qe=datareinx['quqantity_electricity']
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']
    
    ddm10=ddata[ddata[:,1]==1] #行程段
    ddm10=ddm10[ddm10[:,11]>10]
    ddm10=ddm10[ddm10[:,11]<100]
    
    ##仅处理10-300公里的的行程段
    cf=[]
    ce=[]
    cs=[]
    tcc=[]
    for i in range (ddm10.shape[0]):
        a=int(ddm10[i,2]) #索引
        b=int(ddm10[i,3]) #索引
        
        fcc=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
        fce=qep.loc[a]-qep.loc[b] #soc
        tccc=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b])/3600 #换算成小时
        daa=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
        dau=da.loc[a:b-1].reset_index(drop=True) 
        fcb=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
        fca=sum((daa-dau)*fcb/100) # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量（毫升）

#        print(daa)
        

        tcc.append(tccc)
        cf.append(fcc) #电池剩余能量
        ce.append(fca) #使用燃油量
        cs.append(fce) #soc变化
    cd=ddm10[:,11]  #里程
    return cf,ce,cd,cs,tcc

#fig = plt.figure()
#ax=fig.add_subplot(111)
#ax.scatter(ce,cf)
#plt.show()
def ct2(ddata,datareinx):
    import numpy as np
    import getTimeDiff
    qe=datareinx['quqantity_electricity']
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']

    ddm10=ddata[ddata[:,1]==1] #行程段
#    ddm10=ddm10[ddm10[:,11]>10]
#    ddm10=ddm10[ddm10[:,11]<100]
    
    ##仅处理10-300公里的的行程段
    cf=[]
    ce=[]
    cs=[]
    cd=[]
    tcc=[]
    soc=[]
    
    cf2=[]
    ce2=[]
    cs2=[]
    cd2=[]
    tcc2=[]
    soc2=[]
    
    
    for i in range (ddm10.shape[0]):
        a=int(ddm10[i,2]) #索引
        b=int(ddm10[i,3]) #索引
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
            
            
            cf.append(fcc) #使用的电池能量
            ce.append(fca) #使用燃油量
            cd.append(ddm10[i,11])  #里程
            cs.append(fce) #soc变化
            tcc.append(tccc) #耗时
            soc.append((qep.loc[a]+qep.loc[b])/2)
        ##烧电的
        else:
            fcc2=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
            fce2=qep.loc[a]-qep.loc[b] #soc
            tccc2=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b])/3600 #换算成小时
            daa2=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
            dau2=da.loc[a:b-1].reset_index(drop=True) 
            fcb2=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
            fca2=sum((daa2-dau2)*fcb2/100) # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量

            cf2.append(fcc2) #使用的电池能量
            ce2.append(fca2) #使用燃油量
            cd2.append(ddm10[i,11])  #里程
            cs2.append(fce2) #soc变化
            tcc2.append(tccc2) #耗时
            soc2.append((qep.loc[a]+qep.loc[b])/2)
            
    return cf,ce,cd,cs,tcc,soc,cf2,ce2,cd2,cs2,tcc2,soc2
    #电池能量，燃油量，里程，soc，耗时
#
    dg=np.vstack((np.array(cf),np.array(ce),np.array(cd),np.array(cs),np.array(tcc)))
    dg=np.transpose(dg)
    np.sum(np.array(cf))


##每一个行程拟合一个方程


###计算油耗率
def ct3(ddata,datareinx):
    import getTimeDiff
    qe=datareinx['quqantity_electricity']
    qep=datareinx['quqantity_electricity_percent']
    da=datareinx['distance_accumulative']
    fc=datareinx['fuel_consumption']
    tc=datareinx['time_collect']

    ddm10=ddata[ddata[:,1]==1] #行程段
#    ddm10=ddm10[ddm10[:,11]>10]
#    ddm10=ddm10[ddm10[:,11]<100]
    
    ##仅处理10-300公里的的行程段
    cf=[]
    ce=[]
    cs=[]
    cd=[]
    tcc=[]
    soc=[]

    
    for i in range (ddm10.shape[0]):
        a=int(ddm10[i,2]) #索引
        b=int(ddm10[i,3]) #索引
        '''判断是不是烧油的行程段'''
        
#        ddd_temp=datareinx.loc[a:b]
        if any(fc.loc[a+1:b]>500):  #大于500就是在烧油驱动
        
            fcc=qe.loc[a]-qe.loc[b] #电池剩余能量   #.loc， 行或列只能是标签名。 只加一个参数时，只能进行 行 选择
            fce=qep.loc[a]-qep.loc[b] #soc
            tccc=getTimeDiff.GetTimeDiff(tc.loc[a],tc.loc[b])/3600 #换算成小时
            daa=da.loc[a+1:b].reset_index(drop=True) #distance_accumulative
            dau=da.loc[a:b-1].reset_index(drop=True) 
            fcb=fc.loc[a+1:b].reset_index(drop=True) #fuel_consumption
            fca=sum((daa-dau)*fcb/100)*8.9 # 行驶的距离 * 每百公里燃油消耗量 =燃油消耗量
            
            
            cf.append(fcc) #使用的电池能量
            ce.append(fca) #使用燃油量
            cd.append(ddm10[i,11])  #里程
            cs.append(fce) #soc变化
            tcc.append(tccc) #耗时
            soc.append((qep.loc[a]+qep.loc[b])/2)
        
            
    return cf,ce,cd,cs,tcc,soc