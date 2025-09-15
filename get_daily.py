
import pandas as pd
import tushare as ts

ts.set_token('your token')
pro = ts.pro_api()

stocks = pd.read_csv("stock.csv", dtype=str)
print(stocks.head())

df = pro.daily(trade_date='20250912')  # 获取当天全部A股日行情
df = df.round(2)
print(df.head())
df['ts_code'] = df['ts_code'].str[:6]
print(df.head())

# 合并
df_merged = pd.merge(df, stocks, on='ts_code', how='left')
print(df_merged.head())

df_merged.to_csv("daily.csv", index=False)