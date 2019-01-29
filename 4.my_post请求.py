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
@file: post请求.py
@time: 2019/1/28 13:50
"""

import requests
import json


def post(url, page, ID):
    url = url
    # 参数
    body = {'authorId': ID, 'papersTab': 'authorPaper', 'p': page}
    # 请求头
    headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    # 返回信息
    response = requests.post(url, data=json.dumps(body), headers=headers)
    return response


if __name__ == "__main__":
    for l in range(1, 2):
        html = post('http://med.wanfangdata.com.cn/Author/GetPaperList', l, 'A000000001')
        # 返回信息
        print html.text
        # 返回响应头
        print html.status_code
    print "OK"
