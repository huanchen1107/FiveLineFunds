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
