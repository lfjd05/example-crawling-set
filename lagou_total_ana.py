# -*- coding: utf-8 -*-

""" 作者： 吕祎
    日期：2018.3.15
    功能：拉钩网所有技术相关职位的数据分析
    数据来源：拉钩网
    爬虫：lagou.py
"""

from pandas import read_csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

Data = read_csv("D:/python Programme/crawl/拉钩总.csv", index_col=None, header=0)

# 数据清洗
Data.dropna()

# 各个职位平均薪水
# Data.groupby('职位名称').size().plot(kind='bar')
# plt.show()
