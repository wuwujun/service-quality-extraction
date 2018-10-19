#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time    : 18-10-15 下午9:30 
# @Author  : wuwujun 
# @File    : meituan_analyse.py 
# @Software: PyCharm
# @function: 对美团数据集应用百度api进行标签抽取

import re
import time
import csv
import pandas as pd
from aip import AipNlp
from utils.data_clean import Dataclean

APP_ID = '14443285'
API_KEY = 'eOvXUANku8bGRrKx2XBqAF5N'
SECRET_KEY = 'UCm3RTMXWRIsoxm7NpjasDUrqiSMa2gO'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# 用户评论标签抽取
def tag_extraction(data_save_path):
    options = {'type': 4}  # 餐饮美食类
    prop_adj = {}
    count = 0
    df = pd.read_csv(data_save_path, encoding='utf-8')
    with open('../../results/meituan/error_log.txt', 'w+', encoding='utf-8') as f:
        for text in df.ix[:, 'content']:
            count += 1
            try:
                print(count)
                # 提取中文数字和英文
                text = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', ' ', text)
                result = client.commentTag(text, options)
            except Exception as e:
                f.write('有编码问题的行数：' + str(count) + '\n')
                print('有编码问题的行数：' + str(count))
                print(e)

            if 'items' in result:
                data = result['items']
                for item in data:
                    prop = item['prop']
                    adj = item['adj']
                    # 没有就添加且设置为value为空set，并且返回空set;有就返回不空的set，使用set是为了避免value中出现重复值
                    temp = prop_adj.setdefault(prop, set())
                    if adj:
                        temp.add(adj)
            else:
                f.write('有错误的行数：' + str(count) + ' 错误代码：' + str(result['error_code']) + result['error_msg'] + '\n')
                print(str(result['error_code']) + result['error_msg'])

    tag = prop_adj.keys()
    adjs = list(prop_adj.values())
    for i, item in enumerate(adjs):
        adjs[i] = ','.join(item)
    dataframe = pd.DataFrame(list(zip(tag, adjs)), columns=['tag', 'adj'])  # 解释:https://blog.csdn.net/ginsan/article/details/80998911
    dataframe.to_csv('../../results/meituan/tag.csv', index=False)


# 读取存储好的tag,adj文件
def read_csv():
    # df = pd.read_csv('../../results/meituan/tag.csv')
    # print(df)
    with open('../../results/meituan/tag.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            text = row[1]
            print(type(text))


def main():
    file = 'sentiment_analysis_trainingset.csv'
    path = '/home/shuqianqian/dataset/'  # 服务器上的路径
    dc = Dataclean(filename=file, data_save_path=path)
    new_path = dc.clean_meituan()
    print('DONE==========================')
    start = time.clock()
    tag_extraction(new_path)
    elapsed = (time.clock() - start)
    print('======================Time used: ', elapsed)


if __name__ == '__main__':
    main()
