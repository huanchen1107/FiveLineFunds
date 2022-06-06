# coding: utf-8

from FinMind.data import DataLoader
from datetime import datetime

def load_from_FinMind(buy_list):
    basket_of_stock = {}
    for s in buy_list:
        df = DataLoader.FinData(dataset='TaiwanStockPrice', select=s, date='1700-01-01').set_index('date')                                                                [['open','max','min','close','Trading_Volume', 'Trading_money']]
        df.columns = ['Open','High','Low','Close','Volume','Trading_money']
        df.name = s
        basket_of_stock[s] = df
    return basket_of_stock


