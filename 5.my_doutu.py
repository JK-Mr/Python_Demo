"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.cpm
@site: 
@software: PyCharm
@file: 5.my_doutu.py
@time: 2019/3/8 15:19
"""

from bs4 import BeautifulSoup
import random
import requests
import os

'''
斗图啦爬虫
'''


# 生成随机暂停秒数
def generate_second():
    return random.randint(5, 10)


# 请求
def get(url):
    # 请求头,模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 返回信息
    response = requests.get(url, headers=headers)
    return response


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print('soup type is NoneType')
    return soup


# 发起图片请求
def download(img_name, img_url):
    # print img_url, img_name
    # 本地文件夹名字
    folder = 'F:\doutu'
    if not os.path.exists(folder):  # 如果文件夹不存在
        os.mkdir(folder)  # 创建文件夹
    # 拼接本地图片路径
    path = folder + "\\" + img_name + img_url[-4::]
    # 请求头,模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    # 发起图片请求
    reponse = requests.get(url=img_url, headers=headers)
    # 图片二进制数据
    content = reponse.content
    saveimg(path, content)


# 保存图片
def saveimg(path, content):
    print(path)
    with open(path, 'wb') as f:
        f.write(content)


# 获取页面所需内容
def html_content(html_content):
    content = html_content.select('div[class="page-content text-center"]')[0].select('div')[0]
    for i in content:
        try:
            paper = i.select('img[data-original]')[0]
            # 图片名字
            img_name = paper['alt']
            # 图片url
            img_url = paper['data-original']
            download(img_name, img_url)
        except:
            continue


def loadpage(url, page):
    generate_second()
    html = get(str(url) + str(page))
    html_content(get_soup(html.text))


if __name__ == "__main__":
    for i in range(1, 100):  # 1-100页
        print('爬取第%d页' % i)
        loadpage('https://www.doutula.com/photo/list/?page=', i)
    print('ok')
