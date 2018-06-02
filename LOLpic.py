#!/usr/bin/python
# -*- coding: utf-8 -*-
# author Liuweiqiu

import requests
import re


#获取js字典
def path_js(url_js):
    res_js = requests.get(url_js).content
    html_js = res_js.decode("gbk")
    pat_js = r'"keys":(.*?),"data"'
    enc = re.compile(pat_js)
    list_js = enc.findall(html_js)
    dict_js = eval(list_js[0])
    return dict_js

#从 js字典中提取到key值生成url列表
def path_url(dict_js):
    pic_list = []
    for key in dict_js:
        for i in range(20):
            xuhao = str(i)
            if len(xuhao) == 1:
                num_houxu = "00" + xuhao
            elif len(xuhao) == 2:
                num_houxu = "0" + xuhao
            numStr = key+num_houxu
            url = r'http://ossweb-img.qq.com/images/lol/web201310/skin/big'+numStr+'.jpg'
            pic_list.append(url)
    print(pic_list)
    return pic_list

#从 js字典中提取到value值生成name列表
def name_pic(dict_js, path):
    list_filePath = []
    for name in dict_js.values():
        for i in range(20):
            file_path = path + name + str(i) + '.jpg'
            list_filePath.append(file_path)
    return list_filePath

#下载并保存数据
def writing(url_list, list_filePath):
    try:
        for i in range(len(url_list)):
            res = requests.get(url_list[i], timeout = 15).content
            with open(list_filePath[i], "wb") as f:
                f.write(res)

    except Exception as e:
        print("下载图片出错,%s" %(e))
        return False


if __name__ == '__main__':
    url_js = r'http://lol.qq.com/biz/hero/champion.js'
    path = r'D:\files\py_files\paichong\LOLimg\\'
    dict_js = path_js(url_js)
    url_list = path_url(dict_js)
    list_filePath = name_pic(dict_js, path)
    writing(url_list, list_filePath)


































