# -*- coding: utf-8 -*

"""
@author: Jiang Ke
@license: Apache Licence 
@contact: jiangke9413@qq.cpm
@site: 
@software: PyCharm
@file: 3.my_bulk.py
@time: 2019/1/21 11:18
"""
import os
import json

windows_linux = '\\'
bulk_path = 'F:\\all_bulks\\'  # 写出文件


# 读取文件
def read_file(filePath):
    filesss = []
    for (root, dirs, files) in os.walk(filePath):
        for filename in files:
            filesss.append(os.path.join(root, filename))
    return filesss


# 写入json文件
def writebulkfile(indexlist, pubmedlist, path):
    index_num = len(indexlist)
    exists = os.path.exists(bulk_path)
    filename = path.split("\\")
    filename_len = len(filename)
    filename = filename[filename_len - 1]
    if not exists:
        os.makedirs(bulk_path)
    for i in range(0, index_num):
        with open(bulk_path + filename + "bulk.json", "a+") as f:
            f.write(indexlist[i])
            f.write(pubmedlist[i])


# 读取json，放入list，并写文件
def readwf_data(path, filepaths):
    indexlist = []
    pubmedlist = []
    for ofl in filepaths:
        filename = ofl.split("\\")
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
    writebulkfile(indexlist, pubmedlist, path)


# generate bulk file use by json files
def readinfo(path, filename):
    with open(filename, "r") as f:
        rdl = f.readline()
    return rdl


# 生成bulk json
def generate_json(json_path):
    for (root, dirs, files) in os.walk(json_path):
        listdir = read_file(json_path)
        readwf_data(json_path, listdir)


if __name__ == "__main__":
    for (root, dirs, files) in os.walk("C:\\Users\\jiang\\Desktop\\download"):  # 读取文件
        if len(dirs) > 0:
            for dir in dirs:
                json_path = root + windows_linux + dir
                print(json_path)
                generate_json(json_path)
    print('Over_________')
