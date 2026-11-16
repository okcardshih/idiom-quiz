# 成語闖關

四字主條成語測驗網頁。題型參考《一字千金》的單元：洞燭機先、見微知著、拼字魔方、近義闖關。

- 成語資料：教育部《成語典》（創用CC 姓名標示－禁止改作 3.0 臺灣），釋義、典源與典故說明為原文照錄。
- 產生網頁：`python3 scripts/build.py`，會把 `data/idioms.json` 嵌入 `src/template.html`，輸出單一檔 `index.html`（離線可開）。
- 資料來源重抓：`scripts/extract.py` 讀取教育部下載的 `dict_idioms_2020_20260929.xlsx` 轉成 JSON。

資料筆數：1,642 則四字主條成語。
