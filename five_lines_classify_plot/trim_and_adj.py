#!/usr/bin/env python
# coding: utf-8

from pandas_datareader.yahoo.daily import YahooDailyReader
import pandas as pd
import numpy as np


# In[2]:


# drop the row with any 0 value or NaN
def _trim(df):
    df = df[(df != 0).all(1)]
    df = df.dropna()
    
    return df


# In[3]:


def _get_adj_ratio(sid):
    adj_ratio = YahooDailyReader(sid+'.TW', '1980-01-01', adjust_price=True).read().Adj_Ratio
    adj_ratio.index = adj_ratio.index.to_native_types()
    return pd.Series(adj_ratio[round(adj_ratio.diff(),2) != 0], index=adj_ratio.index).ffill()


# In[4]:


def _adjust_price(df, key):
    adj_ratio = _get_adj_ratio(key)
    df.loc[:, ['Open','High','Low','Close']] = df[['Open','High','Low','Close']].mul(adj_ratio, axis=0)
    df = df.dropna()
    
    return df


# In[5]:


def trim_then_adjust(df, key):
    return _adjust_price(_trim(df), key)

