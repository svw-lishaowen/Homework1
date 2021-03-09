#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
#数据加载
data = pd.read_csv(r'C:\Users\lishaowen\OneDrive - 上汽大众汽车有限公司\黑马\L4\Market_Basket_Optimisation.csv', header = None)
print(data)
print(data.shape)

#遍历,万物transactions
transactions=[]
for i in range(0,data.shape[0]):
    temp=[]
    for j in range(0,data.shape[1]):
        if str(data.values[i,j])!= 'nan':
            temp.append(data.values[i,j])
    transactions.append(temp)
#频繁项集和关联规则
from efficient_apriori import apriori
itemsets, rules = apriori(transactions, min_support=0.02,  min_confidence=0.3)
print("频繁项集：", itemsets)
print("关联规则：", rules)


# In[60]:


from mlxtend.frequent_patterns import apriori as ap1
from mlxtend.frequent_patterns import association_rules
data['ColumnA'] = data[data.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
data_new=pd.DataFrame(data['ColumnA'])
#print(data_new)

data_hot_encoded = data_new.drop('ColumnA',1).join(data_new.ColumnA.str.get_dummies(','))
print(data_hot_encoded.head())

frequent_itemsets = ap1(data_hot_encoded, min_support=0.02, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.3)
#frequent_itemsets = frequent_itemsets.sort_values(by="support" , ascending=False) 
print("频繁项集：", frequent_itemsets)
# 显示全部的列
pd.options.display.max_columns=100
#rules = rules.sort_values(by="lift" , ascending=False) 
rules = rules.sort_values(by="confidence" , ascending=False) 
#print("关联规则：", rules[ (rules['lift'] >= 1) & (rules['confidence'] >= 0.5) ])
print('关联规则：', rules)


# In[ ]:



