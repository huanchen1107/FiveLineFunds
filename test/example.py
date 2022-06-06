from five_lines_classify_plot.from_FinMind import load_from_FinMind
from five_lines_classify_plot.trim_and_adj import trim_then_adjust
import pandas as pd
import numpy as np
from datetime import datetime
from five_lines_classify_plot.classify_and_plot import five_line_classify_and_plot

buy_list = ['0050', '2330', '1215']
data = load_from_FinMind(buy_list)
for sid in data:
    data[sid] = trim_then_adjust(data[sid], sid)
    data[sid].index = [datetime.strptime(d, "%Y-%m-%d").date() for d in data[sid].index]

high_df = pd.DataFrame({date: dicti['High'] for date, dicti in data.items()})
close_df = pd.DataFrame({date: dicti['Close'] for date, dicti in data.items()})
low_df = pd.DataFrame({date: dicti['Low'] for date, dicti in data.items()})   

group1 = five_line_classify_and_plot((close_df - close_df.mean())/close_df.std(), days=200, mode='stock', high=high_df, low=low_df)
group1.describe()


# Funds
## 只選擇富邦可售plot
import pickle
def load_obj(name):
    with open(str(name) + '.pkl', 'rb') as f:
        return pickle.load(f)
fund_price = load_obj('five_lines_classify_plot/fund_nav')
fund_id = load_obj('fund_id')

#若要從fund_id挑, 要加"if fid in fund_price.columns" 因為fund_id 5115個, fund_price(爬蟲抓到的)5017個
fund_price = fund_price[[fid for fid in fund_id[fund_id['富邦可售']]['基金代碼'] if fid in fund_price.columns]]

#先只印 10個
fund_price = fund_price[fund_price.columns[:10]]
group2 = five_line_classify_and_plot((fund_price-fund_price.mean())/fund_price.std(), days=750)
group2.describe()

group2.get_group(4)