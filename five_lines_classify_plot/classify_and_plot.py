#!/usr/bin/env python
# coding: utf-8
import os
import difflib
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime
import math
import numpy as np
import talib
import re

from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets

from selenium import webdriver
from webdrivermanager import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import functools


def _save_obj(obj, name):
    with open(str(name) + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
#讀取pickle檔
def _load_obj(name):
    with open(str(name) + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def _get_the_fund():
    if os.path.exists('fund_id.pkl'):
        fund_id = _load_obj('fund_id')
        return fund_id
    try:
        fund_id = pd.read_excel\
                       ('(O)Yahoo與可售基金連結查詢五線譜.xls.xlsx', sheet_name='Yahoo奇摩基金代碼')[['基金名稱', '基金代碼']]
        富邦可售 = pd.read_excel('(O)Yahoo與可售基金連結查詢五線譜.xls.xlsx', sheet_name='data_20190315101510(富邦可售基金)',\
                         usecols=['名稱']).dropna()['名稱']
    except:
        print("可售基金excel檔須放在package下!")
        raise
    富邦可售 = 富邦可售.apply(lambda x: re.sub(r"\([^)]{8,}\)", "", x))
    基金名稱 = fund_id['基金名稱'].apply(lambda x: x.replace(" ", ""))
    arr = np.array([[difflib.SequenceMatcher(None, n, name).quick_ratio() for name in 基金名稱] for n in 富邦可售])
    index = np.unique(np.array([np.argmax(row) for row in arr]))
    fund_id['富邦可售'] = False
    fund_id.loc[index, '富邦可售'] = True
    _save_obj(fund_id, 'fund_id')
    
    return fund_id

def _STOCH(series, high=None, low=None):
    tmp_df = pd.DataFrame()
    if high is None:
        tmp_df['K'], tmp_df['D'] = talib.STOCH(series, series, series, fastk_period=9)
    else:
        tmp_df['K'], tmp_df['D'] = talib.STOCH(high, low, series, fastk_period=9)
    return tmp_df.dropna()

def _five_lines_cal(data, days, tolerate):
    # if there's no enough data to compute(not mature)
    y = data.iloc[-days:]
    for i,v in y.count().items():
        if(v < days - tolerate):
            y = y.drop(i, axis=1)
            
    X = y.apply(lambda x: pd.Series(range(x.count()), index=x.dropna().index).reindex(x.index).values)

    midy = y.mean(axis=0)
    midx = X.mean()

    beta = (y - midy).mul(X - midx, axis=0).sum()/((X-midx)**2).sum()
    alpha = midy - midx * beta

    
    # 計算中線跟標準差
    
    mid_line = ((X * beta + alpha))
    std = (y - mid_line).std()

    # we only need today data
    return beta, mid_line, std


def _plot(ax, series, m, s):
    ax.plot(series, scaley=False)
    ax.plot(m-2*s, scaley=False)
    ax.plot(m-s, scaley=False)
    ax.plot(m, scaley=False)
    ax.plot(m+s, scaley=False)
    ax.plot(m+2*s, scaley=False)
    
    
def _make_sigma_interval(m, s):
    return [m-2*s, m-s, m, m+s, m+2*s]


def _determine_which_interval(price, interval):
    return np.searchsorted(interval, price)


def _sort_and_trans_to_degree(b):
    return (np.arctan(b.sort_values(ascending=False))/np.pi)*180

def _open_browser():
    URL = 'https://invest.wessiorfinance.com/notation_fund.html'
    path = ChromeDriverManager().download_and_install()[0]
    browser = webdriver.Chrome(executable_path=path)
    browser.get(URL)
    
    return browser

class Button():
    def __init__(self, browser, sid, start_date, end_date):
        self.browser = browser
        self.sid = sid
        self.start_date = start_date
        self.end_date = end_date
        self.button = widgets.Button(description='Link', tooltip = self.sid)
        self.button.style.button_color = '#87CEFA'
        self.button.on_click(self.on_button_clicked)
        
    def on_button_clicked(self, target):
        self.start_date = self.trans_str_date_format(self.start_date)
        self.end_date = self.trans_str_date_format(self.end_date)
        element = self.browser.find_element_by_xpath('//*[@id="Stock"]')
        element.clear()
        element.send_keys(self.sid)
        start_date = self.browser.find_element_by_id('Odate')
        start_date.clear()
        start_date.send_keys(self.start_date)
        end_date = self.browser.find_element_by_id('Edate')
        end_date.clear()
        end_date.send_keys(self.end_date)
        element = self.browser.find_element_by_xpath('//*[@id="draw_btn"]')
        element.click()
        
    def trans_str_date_format(self, str_date):
        str_date = str(str_date).replace("-","")
        return str_date[:4] + '\t' + str_date[4:] + '\t'
    
class exit_button():
    def __init__(self, browser):
        self.browser = browser
        self.button = widgets.Button(description='exit driver')
        self.button.style.button_color = '#DC143C'
        self.button.on_click(self.on_button_clicked)
    
    def on_button_clicked(self, target):
        self.browser.quit()

def _create_exit_button(browser):
    b = widgets.Button(description='Link', tooltip = 'driver.quit()')
    b.on_click(lambda: browser.quit())
    return b

def five_line_classify_and_plot(df, days=750, tolerate=None, mode='fund', high=None, low=None):
    if mode == 'stock':
        assert (high is not None) and (low is not None)
        fund_id = None
    else:
        fund_id = _get_the_fund()
    if tolerate is None:
        tolerate = int(days/4)
    b, m, s = _five_lines_cal(df, days, tolerate)
    
    if mode == 'fund':
        print("\n\033[1m\033[91m Remember to click the red button at bottom when finish using !! \033[0m\n")
    start_date = str(df.index[-days])
    end_date = str(df.index[-1])
    print(start_date, " to ", end_date, '\n')
    
    b = b[b>0]
    b = _sort_and_trans_to_degree(b)
    b = pd.DataFrame(b, columns=['beta'])
    b['section'] = np.digitize(b, [45, 30, 15])+1
    b_group = b.groupby('section')
    today_m = m.apply(lambda x: x[x.notnull()].values[-1])
    sigma_message = ['[ < -2_sigma ]', '[ -2~-1_sigma ]', '[ -1~0_sigma ]', '[ 0~1_sigma ]', '[ 1~2_sigma ]', '[ > 2_sigma ]']
    
    if mode == 'fund':
        browser = _open_browser()
    a_row_of_buttons = []
    
    for key, daf in b_group:
        print("\n--------------\n\\ group > {:2.0f}° \\\n --------------\n".format((4-key)*15))
        print(len(daf))
        for i, sid in enumerate(daf.index):
            if mode == 'fund':
                a_row_of_buttons.append(Button(browser, sid, start_date, end_date).button)
                if len(a_row_of_buttons) == 3:
                    display(widgets.HBox(a_row_of_buttons, layout=widgets.Layout(justify_content = 'space-around', width='102%')))
                    a_row_of_buttons.clear()
            if i%3 == 0:
                fig = plt.figure(figsize=(16, 2*4))
                outer_grid = fig.add_gridspec(1, 3, wspace=0.2)
            inner_grid = outer_grid[i%3].subgridspec(2, 1)
            ax = fig.add_subplot(inner_grid[0])
                
            interval = _determine_which_interval(df[sid][m[sid].last_valid_index()], _make_sigma_interval(today_m[sid], s[sid]))
            if (fund_id is not None) and (fund_id[fund_id['基金代碼'] == sid]['富邦可售'].values.item()):
                plt.title(sid + ' ' + sigma_message[interval] + '\n[Fubon] ' + str(round(b.loc[sid, 'beta'], 2)) + '°')
            else:
                plt.title(sid + ' ' + sigma_message[interval] + '\n' + str(round(b.loc[sid, 'beta'], 2)) + '°')
            plt.xticks([])
            plt.yticks(np.arange(-4,5,1))
            _plot(ax, df[sid][-days:].dropna(), m[sid].iloc[-days:].dropna(), s[sid])
            
            
            ax1 = fig.add_subplot(inner_grid[1])
            plt.xticks([])
            if mode == 'fund':
                ax1.plot(_STOCH(df[sid][-days-9:].dropna()))
            elif mode == 'stock':
                ax1.plot(_STOCH(df[sid][-days-9:].dropna(), high[sid][-days-9:].dropna(), low[sid][-days-9:].dropna()))
            if i%3 == 2:
                plt.show()
                print('\n\n')
        if mode == 'fund':
            if len(a_row_of_buttons) != 0:
                display(widgets.HBox(a_row_of_buttons))
                a_row_of_buttons.clear()
        plt.show()
        print('\n\n')
    if mode == 'fund':
        display(exit_button(browser).button)
    print('\n')
    
    return b_group

