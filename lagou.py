""""
开发者姓名：吕祎
创建日期：2018.3.13
功能    ： 爬取拉钩网的职业数据
版本    ： 使用beatifulSoup 代替正则表达式
"""
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time


# 找到每个职位的小链接
def get_job_list(url_link, headers):
    # url_link = [url_link, ]
    html = requests.get(url_link, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')  # 页面+解析器类型
    # 找到职位名称
    # job_name = soup.find(attrs={'class': 'keyword-wrapper'}).find('input').get('value')
    # 搜索地
    # local = re.findall('>(.*?)<', str(soup.find(attrs={'class': 'current_city_current'})))  # 找到标签的内容
    # 岗位链接
    job_link = []
    for link in soup.find_all('a', class_='position_link'):
        job_link.append(re.findall('href="(.*?)"', str(link))[0])
    # info.append(re.findall('data-company="(.*?)"', str(job_info))[0])
    # print(job_link)
    return job_link


def get_job_info(url_link, headers):
    html = requests.get(url_link, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')  # 页面+解析器类型
    info = []
    # 职位名称
    test = soup.find('span', attrs={'class': 'name'})
    if test is not None:
        info.append(soup.find('span', attrs={'class': 'name'}).string)
        # 薪水
        info.append(soup.find('span', attrs={'class': 'salary'}).string)
        # 工作地点
        info.append(re.findall('>/(.*?)/<', str(soup.find_all('span')[2]))[0])
        # 经验
        info.append(re.findall('>(.*?)/<', str(soup.find_all('span')[3]))[0])
        # 学历
        info.append(re.findall('>(.*?)/<', str(soup.find_all('span')[4]))[0])
        # 兼职
        info.append(re.findall('>(.*?)<', str(soup.find_all('span')[5]))[0])
        # 公司名字
        info.append(soup.find('div', attrs={'class': 'company'}).string)
        # 发展阶段
        a = soup.find_all('i', class_="icon-glyph-trend")[0].next_sibling.replace('\n  ', '')
        info.append(a)
        # 领域
        info.append(soup.find_all('i', class_="icon-glyph-fourSquare")[0].
                    next_sibling.replace('\n   ', ''))
    # print(info)
    return info


if __name__ == '__main__':
    url = 'https://www.lagou.com/'
    headers = {
        # 'Cookie': 'ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRZXF0dwChEEfxtbV2IKFQ4RUBcSdg1PVSgZCVAyCkBVclRCFXMUR1NnGFkUZgoZXkpcQxNFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4RWAVmBxVeS19AEHUJR1x6GFsBYQEibUVncyVyDkBQehFsBFcCIh8WC0QcdQ1GUTYZWQ1jAxNZRVRKHXYNRlV6EV0EYAcUX3JWcxY%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e1ec43fa536c486bb6e62480b1ddd8c9|1496536177759; mt_xid=V2_52007VwMXWllYU14YShBUBmIDE1NVWVNdG08bbFZiURQBWgxaRkhKEQgZYgNFV0FRVFtIVUlbV2FTRgJcWVNcSHkaXQVhHxNVQVlXSx5BEl0DbAMaYl9oUmofSB9eB2YGElBtWFdcGA%3D%3D; __jda=122270672.14951056289241009006573.1495105629.1496491774.1496535400.5; __jdb=122270672.26.14951056289241009006573|5.1496535400; __jdc=122270672; 3AB9D23F7A4B3C9B=EJMY3ATK7HCS7VQQNJETFIMV7BZ5NCCCCSWL3UZVSJBDWJP3REWXTFXZ7O2CDKMGP6JJK7E5G4XXBH7UA32GN7EVRY; __jdu=14951056289241009006573',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    Data = []
    html = requests.get(url, headers=headers)
    # 解析页面
    soup = BeautifulSoup(html.text, 'lxml')  # 页面+解析器类型
    # 各个职位页面
    # print(soup.find(attrs={'class': 'menu_sub dn'}).find_all('a'))
    job_all = []
    for i in (soup.find(attrs={'class': 'menu_sub dn'}).find_all('a')):
        job_all.append(re.findall('href="(.*?)"', str(i))[0])
    # print(job_all)
    # url = job_all[0]  # 选定工作类型
    for url in job_all[33:]:
        for work_url in get_job_list(url, headers):
            # 进入到每个小岗位页面搜索信息
            print('爬', work_url)
            Data.append(get_job_info(work_url, headers))
            time.sleep(30)
    colomn = ['职位名称', '薪水', '工作地', '经验', '学历', '兼职', '公司名字', '发展阶段', '领域']
    df = pd.DataFrame(Data, columns=colomn)
    print(df)
    df.to_csv('拉钩.csv', columns=colomn)
