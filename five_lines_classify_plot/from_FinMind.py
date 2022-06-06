#!/usr/bin/env python
# coding: utf-8

# In[1]:


from FinMind.Data import Load
from datetime import datetime


# In[2]:


def load_from_FinMind(buy_list):
    basket_of_stock = {}
    for s in buy_list:
        df = Load.FinData(dataset='TaiwanStockPrice', select=s, date='1700-01-01').set_index('date')                                                                [['open','max','min','close','Trading_Volume', 'Trading_money']]
        df.columns = ['Open','High','Low','Close','Volume','Trading_money']
        df.name = s
        basket_of_stock[s] = df
    return basket_of_stock


# In[ ]:




