#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas import Series, DataFrame
data = {'语文': [68, 95, 98, 90,80], '数学': [65, 76, 86, 88, 90], '英语': [30, 98, 88, 77, 90]}
df = DataFrame(data, index=['张飞', '关羽', '刘备', '典韦', '许褚'], columns=['语文', '数学', '英语'])
print(df)
# df['总分'] = df.apply(lambda x: x.sum(), axis=1)
# print(df)
print('各科的最高分',df.max())
print('各科的最低分',df.min())
print('各科的平均分',df.mean())
print('各科的方差',df.var())
print('各科的标准差',df.std())
df["总分"] = df.sum(axis=1)
print('按照总分排名',df['总分'].sort_values(ascending=False))


# In[ ]:




