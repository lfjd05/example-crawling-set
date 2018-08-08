import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# 得到租房信息详情页面的url
def get_allurl(generate_allurl):
    get_url = requests.get(generate_allurl, 'lxml')
    if get_url.status_code == 200:
        # re_set = re.compile('<li.*?data-index=.*?>.*?<a target="_blank".*?href="(.*?)"')
        re_set = re.compile('<div class="info clear">.*?<div class="title">.*?<.*?href="(.*?)".*?>')
        re_get = re.findall(re_set, get_url.text)
        print('该页找到的详细链接数量', len(re_get))
        # print(re_get)
        return re_get


def generate_allurl(user_in_nub):
    url = 'https://bj.lianjia.com/ershoufang/pg{}/'
    for url_next in range(1, int(user_in_nub)):
        yield url.format(url_next)


def open_url(re_get):  # 分析详细url获取所需信息,输入为租房信息详细页面的url
    res = requests.get(re_get)
    info = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')  # 构造soup对象
        info.append(soup.select('.main')[0].getText())  # 按照main标签查找，对于classq前面加“.”,id加“#”，返回的是list
        info.append(soup.select('.total')[0].getText())
        # info.append(re.findall('<p class="lf"><i>面积：</i>(.*?)</p>', res.text)[0])  # 不加[0]显示的字符就是list带着中括号
        # info.append(re.findall('<i>位置：</i>.*?<a href.*?>(.*?)</a>', res.text)[0])
        # info.append(re.findall('<i>位置：</i>.*?<a href.*?<a href.*?>(.*?)</a>', res.text)[0])
        # 面积
        info.append(re.findall('<div class="area">.*?<div class="mainInfo">(.*?)平米</div>', res.text)[0])
        # 年代
        info.append(re.findall('<div class="area">.*?<div class="subInfo">(.*?)年.*?</div>', res.text)[0])
        # 户型
        info.append(re.findall('<div class="room">.*?<div class="mainInfo">(.*?)</div>', res.text)[0])
        # 位置
        # 区
        info.append(re.findall('<div class="areaName">.*?<a href=.*?>(.*?)</a>', res.text)[0])
        # 具体
        info.append(re.findall('<div class="areaName">.*?<a href=.*?>.*?<a href=.*?>(.*?)</a>', res.text)[0])
        # 朝向
        info.append(re.findall('<li>.*?<span class="label">房屋朝向</span>(.*?)</li>', res.text)[0])
        # 装修
        info.append(re.findall('<span class="label">装修情况</span>(.*?)</li>', res.text)[0])
        # # 电梯
        info.append(re.findall('<span class="label">配备电梯</span>(.*?)</li>', res.text)[0])
        # # 供暖
        info.append(re.findall('<span class="label">供暖方式</span>(.*?)</li>', res.text)[0])
        # # 产权
        info.append(re.findall('<span class="label">产权年限</span>(.*?)年</li>', res.text)[0])
        print(info)
        return info


def main(url):
    return open_url(url)
    # writer_to_text(open_url(url))  # 储存到text文件
    #pandas_to_xlsx(open_url(url))
    # update_to_MongoDB(list)   #储存到Mongodb


if __name__ == '__main__':
    # user_in_nub = input('输入生成页数：')
    user_in_nub = 3
    Data = []
    for i in generate_allurl(user_in_nub):  # 输出北京全部url页
        for url in get_allurl(i):
            Data.append(main(url))
            time.sleep(2)
    print('数据集大小', len(Data))
    colomn = ['简介', '总价', '面积', '年代', '户型', '区', '位置', '朝向', '装修', '电梯', '供暖', '产权年限']
    df = pd.DataFrame(Data, columns=colomn)
    # print(df)
    df.to_csv('链家二手房.csv', columns=colomn)
