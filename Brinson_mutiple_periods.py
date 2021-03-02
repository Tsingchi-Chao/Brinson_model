#!/usr/bin/env python
# coding: utf-8

# In[152]:


import pandas as pd
from dateutil.relativedelta import relativedelta
import numpy as np


# 代码借鉴：https://blog.csdn.net/qq_43382509/article/details/106029241

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

# # AKH Brinson多期模型

# In[218]:


class AKHModel:
    """AKHModel
    AKHModel is one of Multiple periods Brinson model which is used to decompose the return of a portfolio into allocation return,selection 
    return and interaction return during mutiple periods.
    """
    def __init__(self,res:pd.ExcelFile):
        """
        Args:
            res(pd.ExcelFile):A ExcelFile which includes several sheet and each sheet is a dataframe,the dataframe is the weight and return 
                            matrix. The index is the asset,like cash,equity,bond,commodity or sector
                            ,the columns are"return_bench,return_portf,weight_bench,weight_portf",the return is the return during the period.
                            The sheet name is the date.注意这里的收益指的是日期后一段时间的收益率，如2017年12月31号指的是2017年12月31到
                            2018年6月30号的收益率
        """
        self.res=res
    def transform_data_format(self):
        """
        Returns:
            sectors(list):The sectors,like equity,bond,commodity or different industry.
            td_dates(list):The trade day.
            p_w(pd.DataFrame):Index is datetime,the columns is  different asset like equity,bond,commodity or different industry,the value 
                              is the weight of the asset in portfolio in that day.
            p_r(pd.DataFrame):It's the same with that of p_w but the value is the return.
            b_w(pd.DataFrame):It's the same with that of p_w but the weight is in the benchmark.
            b_r(pd.DataFrame):It's the same with that of p_r but the return is that of the benchmark. 
        """
        sector_set=set()
        td_dates=[]
        for date in self.res.sheet_names:
            td_dates.append(date)  #得到日期序列
            df=pd.read_excel(res,sheet_name=date,index_col=0)
            sector_set=sector_set.union(set(df.index))
        sectors=list(sector_set) #得到行业序列

        p_w=pd.DataFrame(0,index=td_dates,columns=list(sectors))
        p_r=pd.DataFrame(0,index=td_dates,columns=list(sectors))
        b_w=pd.DataFrame(0,index=td_dates,columns=list(sectors))
        b_r=pd.DataFrame(0,index=td_dates,columns=list(sectors))
        
        for date in self.res.sheet_names:
            df=pd.read_excel(res,sheet_name=date,index_col=0)
            for sector in sectors:
                try:
                    p_w.loc[date,sector]=df.loc[sector,'weight_portf']
                    p_r.loc[date,sector]=df.loc[sector,'return_portf']
                    b_w.loc[date,sector]=df.loc[sector,'weight_bench']
                    b_r.loc[date,sector]=df.loc[sector,'return_bench']
                except:
                    continue
        #在权重和收益矩阵中，每个日期对应的收益是指该日期后面6个月的收益，而不是前面六个月的收益，所以这里日期序列向后面再加上一个日期
        td_dates.append(str(pd.date_range(start=td_dates[-1],end=str(pd.Timestamp(td_dates[-1])+relativedelta(months=7))
                                                       [0:10],freq='2Q').tolist()[1])[0:10])
        return sectors,td_dates,p_w,p_r,b_w,b_r

        
    def brison_attribution(self)->pd.DataFrame:
        """
        Returns:A dataframe that includes the 'Total_Excess_Return', 'Allocation', 'Selection', 'Interaction',the index is the date.
        """
        [sectors,td_dates,p_w,p_r,b_w,b_r]=AKHModel.transform_data_format(self)
        ticker = ['R_pp', 'R_pb', 'R_bp', 'R_bb']
        cum_R = pd.DataFrame(0, columns=ticker,index=td_dates).astype('float') # to store the cumulative return
        single_R = pd.DataFrame(0, columns=ticker, index=td_dates).astype('float') # to store the single return of each period
        for d in td_dates:
            if d!=td_dates[-1]: #因为最后一个日期就没有了再后面六个月的数据，所以这里不再放入dataframe中
                for s in sectors:
                    single_R['R_bb'][d] += b_w[s][d] * b_r[s][d]
                    single_R['R_bp'][d] += b_w[s][d] * p_r[s][d]
                    single_R['R_pb'][d] += p_w[s][d] * b_r[s][d]
                    single_R['R_pp'][d] += p_w[s][d] * p_r[s][d]
            for t in ticker:
                #只调取当前日期前面日期的数据，如当前是2018-12-31，那么只需要2018-06-30及之前的数据就可以，06-30的收益率就是06-30到12-31收益率
                for dd in td_dates[0:td_dates.index(d)]:
                    cum_R[t][d] += (cum_R[t][dd] + 1) * single_R[t][td_dates[td_dates.index(dd)]]
                        
        Total_Excess_Return = cum_R['R_pp'] - cum_R['R_bb']
        AR = cum_R['R_pb'] - cum_R['R_bb']
        SR = cum_R['R_bp'] - cum_R['R_bb']
        IR = Total_Excess_Return - AR - SR
        Outcome = pd.DataFrame(list(zip(Total_Excess_Return, AR,SR, IR)),
                           columns=['Total_Excess_Return', 'Allocation', 'Selection', 'Interaction'],
                           index=td_dates)
        return Outcome


# In[ ]:


def main():
    res=pd.ExcelFile(r'./数据/权重收益矩阵.xlsx')
    akh=AKHModel(res)
    df=akh.brison_attribution()
if __name__=='__main__':
    main()

