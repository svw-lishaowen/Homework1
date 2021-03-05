#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

#数据加载
dataset = pd.read_csv(r'C:\Users\lishaowen\OneDrive - 上汽大众汽车有限公司\黑马\L3\SupplyChain\SupplyChain.csv',encoding='unicode_escape')
dataset


# In[2]:


dataset.isnull().sum()


# In[5]:


import matplotlib.pyplot as plt
import seaborn as sns
data=dataset
plt.figure(figsize=(20,10))
sns.heatmap(data.corr(),annot=True,cmap='coolwarm')


# In[6]:


data['Market'].value_counts()


# In[11]:


plt.figure(1)
market=data.groupby('Market')
market['Sales per customer'].sum().sort_values(ascending=False).plot.bar(figsize=(12,6),title='Sales in different Market')
plt.figure(2)
region=data.groupby('Order Region')
region['Sales per customer'].sum().sort_values(ascending=False).plot.bar(figsize=(12,6),title='Sales in different region')
cat=data.groupby('Category Name')
plt.figure(3)
cat['Sales per customer'].sum().sort_values(ascending=False).plot.bar(figsize=(12,6),title='Total Sales in different Category Name')
plt.figure(4)
cat['Sales per customer'].mean().sort_values(ascending=False).plot.bar(figsize=(12,6),title='Average Sales in different Category Name')


# In[13]:


#按照不同的时间维度（年，月，星期，小时）的趋势
temp=pd.DatetimeIndex(data['order date (DateOrders)'])
temp


# In[21]:


#取order date (DateOrders)字段中的year，month,weekday,hour,monthyear
data['order_year']=temp.year
data['order_month']=temp.month
data['order_week_day']=temp.weekday
data['order_hour']=temp.hour
data['order_month_year']=temp.to_period('M')
data[['order date (DateOrders)','order_year','order_month','order_week_day','rder_hour','order_month_year']]


# In[25]:


#按照不同的时间维度（年，月，星期，小时）的趋势
plt.figure(figsize=(10,12))

df_year=data.groupby('order_year')
plt.subplot(4,2,1)
df_year['Sales'].mean().plot(figsize=(12,12),title='Average Sales in years')
#df_year['Sales'].sum().plot(figsize=(12,12),title='Total Sales in years')

df_day=data.groupby('order_week_day')
plt.subplot(4,2,2)
df_day['Sales'].mean().plot(figsize=(12,12),title='Average Sales in weekday')
#df_day['Sales'].sum().plot(figsize=(12,12),title='Total Sales in weekday')

df_hour=data.groupby('order_hour')
plt.subplot(4,2,3)
df_hour['Sales'].mean().plot(figsize=(12,12),title='Average Sales in hour')
#df_hour['Sales'].sum().plot(figsize=(12,12),title='Total Sales in hour')

df_month=data.groupby('order_month')
plt.subplot(4,2,4)
df_month['Sales'].mean().plot(figsize=(12,12),title='Average Sales in month')
#df_month['Sales'].sum().plot(figsize=(12,12),title='Total Sales in month')


# # 用户分层RFM

# In[26]:


data['order date (DateOrders)']=pd.to_datetime(data['order date (DateOrders)'])
#统计最后一笔订单的时间
data['order date (DateOrders)'].max()


# In[27]:


#假设现在是2018-02-01
import datetime
present=datetime.datetime(2018,2,1)
#计算每个用户的RFM指标
data['Order Customer Id'].value_counts()
#Order Customer Id


# In[29]:


data['TotalPrice']=data['Order Item Quantity'] * data['Order Item Product Price']
data[['TotalPrice','Order Item Quantity','Order Item Product Price','Order Item Total']]


# In[33]:


customer_seg=data.groupby('Order Customer Id').agg({'order date (DateOrders)':lambda x:(present-x.max()).days,
                                     'Order Id':lambda x:len(x),
                                     'Order Item Product Price': lambda x:sum(x)})
customer_seg


# In[38]:


#将字段名称改为 R F M
customer_seg.rename(columns={'order date (DateOrders)':'R_Value','Order Id':'F_Value','Order Item Product Price':'M_Value'},inplace=True)
customer_seg


# In[41]:


#比如划分为4个等级 1-4，4为最高等级
quantiles=customer_seg.quantile(q=[0.25, 0.5, 0.75])
quantiles=quantiles.to_dict()
quantiles


# In[43]:


#R_Value 越小越好=> R_Score越大
def R_Score(a,b,c):
    if a<c[b][0.25]:
        return 4
    if a<c[b][0.50]:
        return 3
    if a<c[b][0.75]:
        return 2
    return 1

#F_Value 越大越好=> R_Score越大
def FM_Score(a,b,c):
    if a<c[b][0.25]:
        return 1
    if a<c[b][0.50]:
        return 2
    if a<c[b][0.75]:
        return 3
    return 4


# In[45]:


#新字段 R_Score，用于将R_Value=>[1,4]
customer_seg['R_Score']=customer_seg['R_Value'].apply(R_Score,args=('R_Value',quantiles))

#新字段 F_Score，用于将FM_Value=>[1,4]
customer_seg['F_Score']=customer_seg['F_Value'].apply(FM_Score,args=('F_Value',quantiles))

#新字段 M_Score，用于将FM_Value=>[1,4]
customer_seg['M_Score']=customer_seg['M_Value'].apply(FM_Score,args=('M_Value',quantiles))

customer_seg


# In[53]:


#计算用户RFM分层
def RFM_User(df):
    if df['M_Score']>2 and df['F_Score']>2 and df['R_Score']>2:
        return '重要价值用户'
    if df['M_Score']>2 and df['F_Score']<=2 and df['R_Score']>2:
        return '重要发展用户'
    if df['M_Score']>2 and df['F_Score']>2 and df['R_Score']<=2:
        return '重要保持用户'
    if df['M_Score']>2 and df['F_Score']<=2 and df['R_Score']<=2:
        return '重要挽留用户'
    if df['M_Score']<=2 and df['F_Score']>2 and df['R_Score']>2:
        return '一般价值用户'
    if df['M_Score']<=2 and df['F_Score']<=2 and df['R_Score']>2:
        return '一般发展用户'
    if df['M_Score']<=2 and df['F_Score']>2 and df['R_Score']<=2:
        return '一般保持用户'
    if df['M_Score']<=2 and df['F_Score']<=2 and df['R_Score']<=2:
        return '一般挽留用户'


# In[54]:


customer_seg['Customer_Segmentation']=customer_seg.apply(RFM_User,axis=1)
customer_seg


# In[58]:


customer_seg['Customer_Segmentation'].value_counts()


# In[ ]:




