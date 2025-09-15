# -*- coding: utf-8 -*-

import time

import pandas as pd
from bottle import template


def top_ten_by_price(sub_li):
    """
    股价排名
    """
    sub_li.sort(key=lambda x: float(x[5]), reverse=True)
    return sub_li[0:10]


def top_ten_by_range(sub_li):
    """
    涨幅排名
    """
    sub_li.sort(key=lambda x: float(x[8]), reverse=True)
    return sub_li[0:10]


def top_ten_by_range_r(sub_li):
    """
    跌幅排名
    """
    sub_li.sort(key=lambda x: float(x[8]))
    return sub_li[0:10]


def top_ten_by_volume(sub_li):
    """
    成交量排名
    """
    sub_li.sort(key=lambda x: float(x[9]), reverse=True)
    return sub_li[0:10]


def top_ten_turn_volume(sub_li):
    """
    成交额排名
    """
    sub_li.sort(key=lambda x: float(x[5]), reverse=True)
    return sub_li[0:10]





if __name__ == '__main__':
    TEMPLATE = "template.html"
    INDEX_HTML = "index.html"
    CSV_PATH = "daily.csv"

    df = pd.read_csv(CSV_PATH)
    print(df.head())
    stock_list = df.to_numpy().tolist()
    # print(stock_list)

    price_list = top_ten_by_price(stock_list)
    range_list = top_ten_by_range(stock_list)
    range_r_list = top_ten_by_range_r(stock_list)
    volume_list = top_ten_by_volume(stock_list)
    turn_volume_list = []

    context = dict()
    context["price_list"] = price_list
    context["range_list"] = range_list
    context["range_r_list"] = range_r_list
    context["volume_list"] = volume_list
    context["turn_volume_list"] = turn_volume_list
    context["stock_list"] = stock_list

    html = template(TEMPLATE, items=context)

    with open(INDEX_HTML, 'wb') as f:
        f.write(html.encode('utf-8'))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("=======success========")
        f.close()

