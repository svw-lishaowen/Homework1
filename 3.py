#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
df=pd.read_csv('./car_complain.csv')
dfdf=df.drop('problem',axis=1).join(df.problem.str.get_dummies(','))
df


# In[3]:


df=df.drop('problem',axis=1).join(df.problem.str.get_dummies(','))
df


# In[35]:


def f(x):
    x=x.replace('一汽-大众','一汽大众')
    return x
df['brand']=df['brand'].apply(f)
result=df.groupby(['brand'])['id'].agg(['count'])
result


# In[6]:


tags=df.columns[7:]
tags


# In[36]:


result2=df.groupby(['brand'])[tags].agg(['sum'])
result2


# In[37]:


result2=pd.merge(result,result2,how='left',on=['brand'])
result2


# In[38]:


result2=result2.sort_values('count',ascending=False)
result2


# In[47]:


result3=df.groupby(['brand'])['car_model'].nunique()
result3


# In[ ]:


# 车型投诉总数跟按照品牌投诉总数一样，把按照brand统计的位置改成car_model即可。


# In[48]:


result4=pd.merge(result,result3,how='left',on=['brand'])
result4


# In[50]:


result4['平均车型投诉'] = result4['count'] /result4['car_model']
result4


# In[51]:


result4=result4.sort_values('平均车型投诉',ascending=False)
result4


# In[ ]:




