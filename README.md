---
Title: Fund Recommendation Bot
Summary: 基金推薦系統
Authors: Huan CHen and Chuboy
Date: 2022/06/06 v2
Tags: Python 
---

# Vue+Fastapi
> 另一個更強的結合前端Vue與後端Fastapi的證券交易分析系統：[https://chuboy.dev/stock](https://chuboy.dev/stock/)
> 這一個

## 專案起手式
1.  安裝[miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. 安裝[vscode](https://code.visualstudio.com)
3. 安裝[vscode-python擴充模組](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. vscode快捷鍵`ctrl + ~`，在終端機`pip install -r requirements.txt` 安裝必備套件
5. `python exacrawler.py --tickers`從臺灣證交所下載上市上櫃的列表，整理成`csv/代號.csv`

2. 若是Unix系統(如windows的wsl、mac、linux)，使用指令來同步伺服器檔案
```shell
rsync *.py root@172.105.120.225:/home/admin/tvf/
```

### v1 更新
#### API:

```python
 from five_lines_classify_plot.classify_and_plot import five_line_classify_and_plot


five_line_classify_and_plot 參數說明(可參考example.ipynb):
	df: Close dataframe with datetime.date index, stock_id/fund_id columns
	days: 用幾天算 five lines
	plot_days: 要畫出從今天到多久以前的資料
	tolerate: 從今天往days天前算 可以接受至多多少NaN default為(1/4)*days
	mode: 'fund'(default)/'stock'
	high: High dataframe
	low: Low dataframe

Note:
	1. high/low 在stock mode為必須，fund mode不用，因為沒有基金的最高價 最低價資料(所以在計算KD值變成每天的最高=最低=基金淨值)

	2. 目前斜率在視覺上的問題還不知道如何合適處理

	3. fund_nav.pkl(基金淨值)很久沒有更新了
```


### v2 版更新
1. 加上link button
2. 取消 plot day
3. 修改five line計算
4. 修改對應關係
5. 視覺斜率: 標準化 + scaley = False
6. 使用webdriver-manager管理driver版本(link button用的)
