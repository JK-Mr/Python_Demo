# -*- coding: utf-8 -*-

"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.cpm
@site: 
@software: PyCharm
@file: 2.my_wanfang.py
@time: 2019/1/15 16:08
"""

"""
    1.根据url获取到页面里的论文链接
"""

from bs4 import BeautifulSoup
import requests
import json
import random

# 文件路径
file = 'F:\\data.json'


# 生成随机暂停秒数
def generate_second():
    """
    :return: 生成随机暂停秒数
    """
    return random.randint(10, 15)


# post请求
def post(url, page, ID):
    url = url
    body = {'authorId': ID, 'papersTab': 'authorPaper', 'p': page}
    headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    # 返回信息
    return response


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print
        'soup type is NoneType'
    return soup


# 获取页面所需内容
def html_content(html_content):
    content = html_content.select('li[class="clear"]')
    for i in content:
        try:
            paper_url = i.select('div[class="author-list-title"]')[0].select('a')[0]['href']
            # 调用写入文件方法
            writeTheFile(file, paper_url)
            # 调用读取文件方法
            # readFile(file)
        except:
            continue


# 写入文件
def writeTheFile(file, paper_url):
    with open(file, 'a+') as f:  # 设置文件对象
        f.write(paper_url + '\n')
        return paper_url


# 读取文件
def readFile(file):
    with open(file, 'r') as f:
        f.readline()
        return f.readline()


# 获取ID
def ID(idStart, idOver, pageStart, pageOver):
    for i in range(idStart, idOver):
        b = len(str(i))
        ID = ''
        if b == 1:
            ID = 'A00000000%d' % i
        elif b == 2:
            ID = 'A0000000%d' % i
        elif b == 3:
            ID = 'A000000%d' % i
        elif b == 4:
            ID = 'A00000%d' % i
        elif b == 5:
            ID = 'A0000%d' % i
        elif b == 6:
            ID = 'A000%d' % i
        elif b == 7:
            ID = 'A00%d' % i
        pageNumber(ID, pageStart, pageOver)


# 获取页码
def pageNumber(ID, pageStart, pageOver):
    for l in range(pageStart, pageOver):
        # 间隔时间
        generate_second()
        # 发送post请求
        html = post('http://med.wanfangdata.com.cn/Author/GetPaperList', l, ID)
        if html.status_code == 200:
            html_content(get_soup(html.text))
        else:
            continue

        print('页面连接是：http://med.wanfangdata.com.cn/Author/General/' + ID + '' + '页码是：%d' % l)


if __name__ == "__main__":
    # 前两位id指定范围
    # 后两位页码指定范围
    ID(999999, 1000000, 1, 2)
    print('Over_________')
