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
6. `python3 crawler.py --history`從Yahoo Finance下載價格資料庫(會先讀取`csv/代號.csv`)，獲得每檔台股自2000年的資料，也可從[谷歌雲端](https://drive.google.com/file/d/1lQ8CU27t8WCdIhc8SFV8JbE__fmt0SnH/view?usp=sharing)下載
7. `python3 crawler.py --merged`從公開資訊觀測站下載每季四大財務彙總報表(IFRS後)
8. `python3 fin_trading.py --season`從價格資料庫整理出每季季末價
9. `python3 fin_trading.py --merge-csv`合併每季四大財務彙總報表與季末價
10. `python3 fin_trading.py --backtest`訓練模型、繪圖檢視績效、儲存模型權重
11. `python3 fin_trading.py --predict`讀財報(快取)、合併最新價格、讀取模型權重、推薦買賣策略
12. `python3 server.py --debug`啟動站台，完成後造訪 http://localhost:5000/stock/docs 查看API文件
13. 每日資料更新的動作會交由`crontab`定時執行`python3 crawler.py --close`的動作
14. `python3 auto_md2html.py`把當前目錄下所有`.md`檔轉換成`.html`，並產生部落格的版面

## 專案部屬
1. 若是Windows系統，下載軟體[WinSCP](https://winscp.net/eng/download.php)透過`scp`協定將檔案拖曳至遠端伺服器，或在git bash內用指令安裝rsync
```shell
curl -O https://repo.msys2.org/msys/x86_64/rsync-3.2.3-1-x86_64.pkg.tar.zst --insecure
zstd -d rsync-3.2.3-1-x86_64.pkg.tar.zst
tar -xf rsync-3.2.3-1-x86_64.pkg.tar
cp usr/bin/rsync.exe C:/Program Files/Git/usr/bin
```
2. 若是Unix系統(如windows的wsl、mac、linux)，使用指令來同步伺服器檔案
```shell
rsync *.py root@172.105.120.225:/home/admin/tvf/
```
3. 在`apache`或`nginx`代理伺服器中，設定網址的redirect，指定到`server.py`所使用的連接阜，如5000
`nano /etc/nginx/sites-available/default`
```nginx
server {
	listen 80;
	listen 443 ssl default_server;
	listen [::]:443 ssl default_server;
	ssl on;
	ssl_certificate /etc/ssl/www_chuboy_dev.crt;
	ssl_certificate_key /etc/ssl/chuboy_dev.key;

	server_name chuboy.dev www.chuboy.dev;
	root /home/admin/dist;
	index index.html;
	location /stock/ {
		proxy_pass http://localhost:5000;
	}
}
```
4. 為了快速開關伺服器，可用背景執行指令`nohup`啟動服務，並寫成一個`restart.sh`利於手動重啟
```shell
cd /home/admin/tvf
kill -9 `cat server_pid.txt`
nohup uvicorn server:app --port 5000 > server.log 2>&1 & echo $! > server_pid.txt
```

#� �F�i�v�e�L�i�n�e�F�u�n�d�s�
�
�
