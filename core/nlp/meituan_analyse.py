#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time    : 18-10-15 下午9:30 
# @Author  : wuwujun 
# @File    : meituan_analyse.py 
# @Software: PyCharm
# @function: 对美团数据集应用百度api进行标签抽取


import pandas as pd
from aip import AipNlp
from utils.data_clean import Dataclean

APP_ID = '14443285'
API_KEY = 'eOvXUANku8bGRrKx2XBqAF5N'
SECRET_KEY = 'UCm3RTMXWRIsoxm7NpjasDUrqiSMa2gO'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def tag_extraction(data_save_path):
    options = {'type': 4}  # 餐饮美食类
    df = pd.read_csv(data_save_path, nrows=10, encoding='utf-8')
    for text in df.ix[:, 'content']:
        result = client.commentTag(text, options)
        data = result['items']
        for item in data:
            print(item['prop'] + item['adj'])
        print(result)


def main():
    file = 'sentiment_analysis_trainingset.csv'
    path = '/home/wuwujun/Documents/Dataset/'
    dc = Dataclean(filename=file, data_save_path=path)
    new_path = dc.clean_meituan()
    tag_extraction(new_path)


if __name__ == '__main__':
    main()
