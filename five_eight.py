import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


# 得到租房信息详情页面的url
def get_allurl(generate_allurl):
    get_url = requests.get(generate_allurl, 'lxml')
    if get_url.status_code == 200:
        soup = BeautifulSoup(get_url.text, 'lxml')
        re_set = re.compile('<a href="(.*?)"')
        re_get = re.findall(re_set,  soup.select('.des').getText())
        # print('该页找到的详细链接', len(re_get))
        # print(re_get)
        return re_get


def generate_allurl(user_in_nub):
    url = 'http://bj.58.com/chuzu/pn{}/?PGTID=0d3090a7-0000-1afc-9c62-05464eabf2e8&ClickID=2'
    for url_next in range(1, int(user_in_nub)):
        yield url.format(url_next)


def open_url(re_get, header):  # 分析详细url获取所需信息,输入为租房信息详细页面的url
    res = requests.get(re_get, headers=header)
    info = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')  # 构造soup对象
        info.append(re.findall('\r(.*?)\xa0', soup.select('.des')[0].getText().replace('\n', '').replace(' ', ''))[0])  # 按照main标签查找，对于classq前面加“.”,id加“#”，返回的是list
        info.append(soup.select('.room')[0].getText().replace('\n','').replace(' ', ''))
        info.append(soup.select('.add')[0].getText().replace('\n', '').replace('\r', ''))
        info.append(str(soup.find('div', attrs={'class': 'money'}).find('b')).replace('<b>', '').replace('</b>', ''))
        # print(info)
        return info


def main(url, header):
    return open_url(url, header)
    # writer_to_text(open_url(url))  # 储存到text文件
    #pandas_to_xlsx(open_url(url))
    # update_to_MongoDB(list)   #储存到Mongodb


if __name__ == '__main__':
    # user_in_nub = input('输入生成页数：')
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    user_in_nub = 2
    Data = []
    for i in generate_allurl(user_in_nub):  # 输出北京全部url页
        Data.append(main(i, header))

    print('数据集大小', len(Data))
    colomn = ['简介', '户型', '位置', '价格']
    df = pd.DataFrame(Data, columns=colomn)
    print(df)
    df.to_csv('58租房.csv', columns=colomn)
