import tushare as ts


def replace_code(x):
    if x.endswith('.SZ'):
        return 's_sz' + x[:-3]
    else:
        return 's_sh' + x[:-3]


pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code')
data['ts_code'] = data['ts_code'].apply(replace_code)
print(data)
data.to_csv("stock.csv", index=False)
