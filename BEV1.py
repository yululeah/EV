# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 03:58:33 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:10:30 2018

@author: XPS
"""

import data_processing
import numpy as np
import pandas as pd
import time
import os
import transn



path1=r'/Users/apple/Desktop/shakalaka/research_on_EV/data/bev16/'#0004_3_0'+str(i)+'.txt' 
#path1=r'D:/1/1/1/chun/' 师姐
file_list=[]
for file_name in os.listdir(path1):
    file_list.append(file_name)

time_start=time.time()
names=locals()
for i in range (1,len(file_list)):
    fp=path1+file_list[i]
    #names['df%s'%i]=data_processing.loadData3(fp)
    df=data_processing.loadData3(fp)
        
    if len(df)==0 or len(np.unique(np.array(df['longitude'])))==1 :
        print('kickoffdata',i)
        continue
    else:
        ddata,datareinx = transn.datac(df)
        aa=pd.DataFrame(ddata)
        bb=pd.DataFrame(datareinx)
#        name='D:/1/bevdata2/ddatac'+str(i)+'.csv'师姐
#        name1='D:1/bevdata2/datareinx'+str(i)+'.csv'师姐
        name='/Users/apple/Desktop/shakalaka/research_on_EV/data/ddatac/bev/ddatac'+str(i)+'.csv'
        name1='/Users/apple/Desktop/shakalaka/research_on_EV/data/datareinx/bev/datareinx'+str(i)+'.csv'
        aa.to_csv(name,index=False)
        bb.to_csv(name1,index=False)

    print(i)
    print(time.time()-time_start)



#def savedd(data):
#    aa=pd.DataFrame(data)
#    name='D:/1/r0103/gg0104.csv'
#    aa.to_csv(name,index=False)
        