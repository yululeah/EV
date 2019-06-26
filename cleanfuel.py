# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 20:53:02 2018

@author: anita
"""

def task3(dataframe,ddata):
    """
    输出：清洗后的ddata
    """
    import numpy as np
    dataframe_value = dataframe[['quqantity_electricity_percent','fuel_consumption']].values
    delete_index=[]
    for i in range(ddata.shape[0]):
        if ddata[i,1] == 1:
            Start_index = int(ddata[i,2])
            Stop_index = int(ddata[i,3])
            dataframe_copy = dataframe_value[Start_index:Stop_index+1,:]
            dataframe_copy = dataframe_copy[dataframe_copy[:,1]==0,:] #fuel_consumption为0
            dataframe_copy = dataframe_copy[dataframe_copy[:,0]<15,:] #quqantity_electricity_percent小于15
            if len(dataframe_copy)!=0:
                delete_index.append(i)

           
    return np.delete(ddata,delete_index,axis=0)

#ab=task3(dd2[1],dd2[0])