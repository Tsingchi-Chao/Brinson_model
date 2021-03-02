#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from WindPy import *
w.start()
from dateutil.relativedelta import relativedelta


# 代码借鉴：
# https://blog.csdn.net/m0_47781094/article/details/111691079

# # 计算基准和组合权重收益矩阵

# 一、 计算基准权重收益矩阵
# 
# 1.先求出基准中每支股票的半年度收益率。
# 
# 2.按照wind一级行业划分，通过权重求出行业的收益率。
# 
# 二、 计算组合权重收益矩阵
# 
# 1.求出积极投资重仓股的wind一级行业并与指数投资合并到一起。
# 
# 2.求出每支股票的半年度收益率。
# 
# 3.按照wind一级行业划分，求出行业收益率。
# 

# # BF Brison单期模型

# In[2]:


class BFModel:
    """BFModel
    BFModel is used to decompose the excess return of  portfolio into allocation,selection.
    """
    def __init__(self,data:pd.DataFrame):
        """
        Args: 
            data(pd.DataFrame): A dataframe of the weight and return matrix. The index is the asset,like cash,equity,bond,commodity or sector
                                ,the columns are"return_bench,return_portf,weight_bench,weight_portf",the return is the return during the period.
                                注意这里的收益指的是日期后一段时间的收益率，如2017年12月31号指的是2017年12月31到2018年6月30号的收益率
        """
        self.data=data
        
    def brison_attribution(self)->pd.DataFrame:
        """
        Returns:
            pd.DataFrame: Index is the the asset and "AR_sum,SR_sum,excess_return",which means the allocation return,selection return and excess
            return. The columns are "return_bench,return_portf,weight_bench,weight_portf,AR,SR",AR means the allocation return,SR means the selection return.
        """
        df=self.data.copy()
        return_benchmark=(df['weight_bench']*df['return_bench']).sum()  #The return of the benchmark during the single period.
        df['AR']=(df['weight_portf']-df['weight_bench'])*(df['return_bench']-return_benchmark)
        df['SR']=df['weight_portf']*(df['return_portf']-df['return_bench'])
        df.loc['AR_sum','return_bench']=df['AR'].sum()
        df.loc['SR_sum','return_bench']=df['SR'].sum()
        df.loc['excess_return','return_bench']=df.loc['AR_sum','return_bench']+df.loc['SR_sum','return_bench']
        return df


# In[4]:


def main():
    df=pd.read_excel()  #读取权重收益矩阵数据
    bf_model=BFModel(df)
    data=bf_model.brison_attribution()
    print(data)
if __name__=='__main__':
    main()

