# -*- coding: utf-8 -*-

import csv
import numpy as np
import time
from bottle import template
import requests

"""

github: https://github.com/geeeeeeeek/py_stock

"""


def top_ten_by_price(sub_li):
    """
    股价排名
    """
    sub_li.sort(key=lambda x: float(x[1]), reverse=True)
    return sub_li[0:10]


def top_ten_by_range(sub_li):
    """
    涨幅排名
    """
    sub_li.sort(key=lambda x: float(x[3]), reverse=True)
    return sub_li[0:10]


def top_ten_by_range_r(sub_li):
    """
    跌幅排名
    """
    sub_li.sort(key=lambda x: float(x[3]))
    return sub_li[0:10]


def top_ten_by_volume(sub_li):
    """
    成交量排名
    """
    sub_li.sort(key=lambda x: float(x[4]), reverse=True)
    return sub_li[0:10]


def top_ten_turn_volume(sub_li):
    """
    成交额排名
    """
    sub_li.sort(key=lambda x: float(x[5]), reverse=True)
    return sub_li[0:10]


def request_to_list(r_flatten_list, group_step):
    r_stock_list = []
    # 分组处理, 步长group_step
    for i in range(0, len(r_flatten_list), group_step):
        print("request index=%d" % i)
        sub_list = r_flatten_list[i:i + group_step]
        sub_flatten_str = ",".join(sub_list)
        r = requests.get("http://hq.sinajs.cn/list=" + sub_flatten_str)
        if r.status_code == 200:
            # print "=======", str(i), "success========"
            split_lines_list = r.text.splitlines()

            for line in split_lines_list:
                stock_id = line[line.find("=") - 8:line.find("=")]
                # 格式: var hq_str_sh201004="R091,0.000,4.450,4.450,2019-02-20,11:30:00,03";
                # 分离等号后面的字段
                right_str = line[line.find("\"") + 1:line.rindex("\"")]
                if len(right_str) > 0:
                    stock_field_list = right_str.split(",")
                    stock_field_list[1] = round(float(stock_field_list[1]), 2)
                    if stock_field_list[1] > 0:
                        stock_field_list.append(stock_id)
                        r_stock_list.append(stock_field_list)

    return r_stock_list


if __name__ == '__main__':
    TEMPLATE = "template.html"
    INDEX_HTML = "index.html"
    CSV_PATH = "stock.csv"

    with open(CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

        # list扁平化 [['a'],['b'],['c']] ==> ['a','b','c']
        flatten_list = np.array(your_list).flatten().tolist()
        del flatten_list[0]

        stock_list = request_to_list(flatten_list, 50)

        price_list = top_ten_by_price(stock_list)
        range_list = top_ten_by_range(stock_list)
        range_r_list = top_ten_by_range_r(stock_list)
        volume_list = top_ten_by_volume(stock_list)
        turn_volume_list = top_ten_turn_volume(stock_list)

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
