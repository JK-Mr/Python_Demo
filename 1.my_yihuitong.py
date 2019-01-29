# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.cpm
@site: 
@software: PyCharm
@file: 1.my_yihuitong.py
@time: 2019/1/8 13:31

"""

"""
思路：
    1.根据url获取到页面里的html
    2.根据html内容解析为soup（utf-8编码）
    3.获取需要的字段
        1.获取 title
        2.获取 url
    4.把url转换成uu_id
    5.获取时间
    6.获取主要内容
        1.去掉回车
    7.编译成json文件的格式
        1.获取当时时间，转成yymmdd格式
    8.生成每日的bulk json
        1.读取生成的文件，添加到一个文件内
        2.循环获取文件把每个文件写入到bulk json
"""

from bs4 import BeautifulSoup
import requests as req
import json
import time
import datetime
import random
import os
import redis
import uuid

# 爬取的类型
json_newsType = '医学指南'
# 爬取的网站
source_wb = '医脉通'
# 使用的库，  和库中比对看是否存在
db_num = 18
# 数据类型
newsType = 'yimaitong'
# 头部消息
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
pool = redis.ConnectionPool(host='47.104.101.207', port=6379, decode_responses=True, db=db_num, password='Pa88####')
r = redis.Redis(connection_pool=pool)
# json文件
path__ = 'C:\\Users\\jiang\\Desktop\\yimaitong\\'
# pak文件
json__path = 'C:\\Users\\jiang\\Desktop\\json_yimaitong\\'
windows_linux = '\\'


# 生成随机暂停秒数
def generate_second():
    """
    :return: 生成随机暂停秒数
    """
    return random.randint(5, 15)


# 去掉回车
def replace_rnb(txt):
    """
    去掉，\r（回车）、\n（换行）、\t（横向制表符）
    :param txt: 带有回车的值
    :return: 去掉回车的值
    """
    return txt.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').strip()


# 去掉空格 none
def replace_blank(txt):
    """
    :param txt: 带有空格的值
    :return: 去掉空格的值
    """
    rep_blk = txt.replace(' ', '')
    return rep_blk.replace('None', '')


# json文件的格式
def build_json(title, son_url, uu_id, time_date, content):
    resources = {}
    resources['keyWords'] = ['暂无信息']
    resources['title'] = title
    resources['article_id'] = uu_id
    resources['pub_person'] = source_wb
    resources['article_content'] = content
    resources['pub_time'] = time_date
    resources['article_author'] = source_wb
    resources['author_level'] = '暂无信息'
    resources['author_hospital'] = '暂无信息'
    resources['author_dept'] = '暂无信息'
    resources['url'] = son_url
    resources['source'] = source_wb
    resources['type'] = json_newsType
    resources['zone_url'] = '暂无信息'
    resources['uuid'] = '暂无信息'
    resources['status'] = '0'
    resources['web_source'] = source_wb
    resources['hco_id'] = '暂无信息'
    resources['hcp_id'] = '暂无信息'
    resources['type_1'] = '暂无信息'
    resources['type_2'] = '暂无信息'
    resources['type_3'] = '暂无信息'
    resources['type_4'] = '暂无信息'
    resources['type_5'] = json_newsType
    resources['source_1'] = '暂无信息'
    resources['source_2'] = '暂无信息'
    return resources


# 获取html 页面内容
def getHtml(url):
    try:
        time.sleep(generate_second())
        r = req.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        encoding = r.encoding
        if encoding is None:
            return r.content
        data = r.content.decode(encoding, 'ignore').encode('utf-8')
        r.close()
        if data is None:
            print 'data is None'
            data = getHtml(url)
        return data
    except Exception as e:
        return getHtml(url)


# 根据html内容解析为soup（utf-8编码）
def get_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup is None:
        soup = get_soup(html_content)
        print 'soup type is NoneType'
    return soup


# 获取title
def get_title(soup):
    try:
        title = soup.select('h1[class="text_title"]')[0].text
        title = replace_rnb(title)
        return title
    except:
        return None


# 把每一篇文章写成json文件
def write_the_file(resources, uu_id):
    today = get_now_date_str()
    file_path = path__ + today
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(file_path + windows_linux + uu_id + '.json', 'w') as f:
        f.write(json.dumps(resources, ensure_ascii=False).decode('utf8'))
        f.close()


# 获取今日的时间
def get_now_date_str():
    replace_date = get_today_date()
    today = newsType + replace_date
    return today


# 获取今日时间格式
def get_today_date():
    now_time = datetime.datetime.now()
    strftime = now_time.strftime('%Y-%m-%d')
    replace_date = strftime.replace('-', '')
    return replace_date


# 把url转换成uu_id
def put_url_redis(url):
    url = url.encode('utf-8')
    rel_url = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
    r.set(rel_url, 'ok')


# 读取文件，添加到一个文件内
def read_file(filePath):
    filesss = []
    for (root, dirs, files) in os.walk(filePath):
        for filename in files:
            filesss.append(os.path.join(root, filename))
    return filesss


# 生成每日的bulk json
def generate_json():
    today = get_now_date_str()
    # 生成当前时间
    path = path__ + today
    listdir = read_file(path)
    jsonpath = json__path + today + windows_linux
    readwf_data(path, jsonpath, listdir)


# 读取json，放入list，并写文件
def readwf_data(path, jsonpath, filepaths):
    indexlist = []
    pubmedlist = []
    for ofl in filepaths:
        filename = ofl.split("/")
        filename_len = len(filename)
        filename = filename[filename_len - 1]
        id = filename.split(".json")
        s = readinfo(path, ofl)
        jsoninfo = json.loads(s)
        arc_id = jsoninfo['article_id']
        if len(id[0]) > 0:
            first = {"index": {"_id": arc_id}}
            fdum = json.dumps(first, ensure_ascii=False).decode('utf-8')
            indexlist.append(fdum + "\n")
            pubmedlist.append(readinfo(path, ofl) + "\n")
    writebulkfile(indexlist, pubmedlist)


# 生成json文件使用的批量文件
def readinfo(path, filename):
    with open(filename, "r") as f:
        rdl = f.readline()
    return rdl


# 写入json文件
def writebulkfile(indexlist, pubmedlist):
    index_num = len(indexlist)
    today = get_today_date()
    file_path = json__path + today + windows_linux
    exists = os.path.exists(file_path)
    if not exists:
        os.mkdir(file_path)
    for i in range(0, index_num):
        with open(file_path + newsType + today + "bulk.json", "a+") as f:
            f.write(indexlist[i])
            f.write(pubmedlist[i])


# 解析html 获取字段
def parseHtml(son_url):
    soup = get_soup(getHtml(son_url))
    # 获取 title
    title = get_title(soup)
    if title is not None:
        # url编码成utf-8
        url = son_url.encode('utf-8')
        # 把url转换成uu_id
        uu_id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
        # 获取时间
        time_date = soup.select('div[class="one_info clearfix"]')[0].select('p')[0].text
        # 获取主要内容
        cont = soup.select('div[class="one_info2"]')[1].text
        content = replace_rnb(cont)
        # 编译成json文件的格式
        resources = build_json(title, son_url, uu_id, time_date, content)
        # 把每一篇文章写成json文件
        write_the_file(resources, uu_id)
        # 把url转换成uu_id
        put_url_redis(son_url)


# 转成utf-8格式再转成uuid
def is_exist(url):
    url = url.encode('utf-8')
    rel_url = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
    return r.exists(rel_url)


def do_clawer(urls):
    for url in urls:
        # exist是否存在
        exist = is_exist(url)
        print url
        if exist:
            continue
        else:
            parseHtml(url)


if __name__ == '__main__':
    url_pre = 'http://guide.medlive.cn/guideline/'
    urls = []
    for i in range(6475, 6480):
        url = url_pre + str(i)
        urls.append(url)
    do_clawer(urls)
    generate_json()
    print 'Over_________'
