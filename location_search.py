# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 14:20:35 2018

@author: anita
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:55:02 2018

@author: anita
"""
import numpy as np
import pandas as pd

'''一串经纬度序列，返回最为聚集的一个位置以及其聚集的百分比,经纬度序列是panda的dataframe形式'''

def locatsearch(lonlat):
    import latlon
    m=1000#距离的误差参数
    aa=np.zeros((lonlat.shape[0],))
    lonlat['count']=pd.Series(aa, index=lonlat.index)
    lonlatarr=np.array(lonlat)
    for i in range(lonlat.shape[0]):
        cut=0
        for j in range(lonlat.shape[0]):
            ds=latlon.haversine(lonlatarr[i,0],lonlatarr[i,1],lonlatarr[j,0],lonlatarr[j,1])
            if ds<m:
                cut=cut+1
        lonlatarr[i,2]=cut/lonlat.shape[0]  #所占的比例
    res=pd.DataFrame(lonlatarr,index=lonlat.index)
    res=res.sort_values(axis=0,ascending=False,by=2)  #排序sort_values；axis：0按照行名排序；1按照列名排序；ascending：默认True升序排列；False降序排列；by：按照那一列数据进行排序
    resg=res.iloc[0:int(round(res.iloc[0,2]*lonlat.shape[0])),:]   #iloc函数：通过行号来取行数据
    return resg,len(res)
            
    
    
#    cal_home_distance=np.eye(lonlat.shape[0])
#    cal_workspace_distance=np.eye(lonlat.shape[0])
#    for i in range(lonlat.shape[0]):
#        for j in range(lonlat.shape[0]):
#            cal_home_distance[i,j]=latlon.haversine(lonlat[i,0],lonlat[i,1],lonlat[j,0],lonlat[j,1])
#    sortcount1=np.zeros((lonlat.shape[0],2))
#
#  
#    for i in range(lonlat.shape[0]):
#        sortcount1[i,0]=i
#
#        for j in range(lonlat.shape[0]):
#            if cal_home_distance[i,j]<=m: 
#                sortcount1[i,1]+=1
#
#
#    sortcount1=sortcount1[np.lexsort(-sortcount1.T)]
#
#    place_final=lonlat[int(sortcount1[0,0]),:]
#
#    place_percent=sortcount1[0,1]/lonlat.shape[0]
##    return sortcount1

    return place_final,place_percent