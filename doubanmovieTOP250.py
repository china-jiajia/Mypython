#!/usr/bin/python
# -*- coding: utf-8 -*-
# author Liuweiqiu


import requests
import re
import csv

#获取资源并下载
def resp(listURL ,path):
    j = 0
    for urlPath in listURL:
        #获取网页源代码
        response = requests.get(urlPath)
        html = response.text

        # 正则表达式
        textPat = r'<em class="">(.*?)</em>'
        namePat = r'alt="(.*?)" src='
        imgPat = r'src="(.*?)" class='

        # 匹配正则（排名、电影名、电影海报（图片））
        listContent = []
        listCont = []
        res = re.compile(textPat)
        res2 = re.compile(namePat)
        res3 = re.compile(imgPat)
        textList = res.findall(html)
        textList2 = res2.findall(html)
        textList3 = res3.findall(html)

        #将排名列表和电影名列表存入一个空列表，以便存入字典
        for i in range(25):
            listCont.append(textList[i])
            listCont.append(textList2[i])
            listContent.append(listCont)
            listCont = []

        # 将“排名和电影名”列表存入字典
        paimingDict = {}
        for i in range(len(textList)):
            paimingDict[textList[i]] = textList2[i]


        #将字典内容写入top250.txt文档中
        mulstr = str(paimingDict)
        with open(r"E:\Py\paichong\doubanmovie\top250.txt", "ab") as f:
            f.write(mulstr.encode())

        #将图片下载到指定的文件夹中
        for i in range(len(textList3)):
            num = i + 1 + j*25
            response = requests.get(textList3[i], verify=False).content
            file_path = path + str(num) + '.jpg'
            with open(file_path, "wb") as f1:
                f1.write(response)
        j += 1

        #写入csv文件
        # with open(r"E:\Py\paichong\doubanmovie\top250.csv", "a") as f:
        #     writer = csv.writer(f)
        #     for content in listContent:
        #         writer.writerow(content)

#top250所有网页网址
def page(url):
    urlList = []
    for i in range(10):
        num = str(25*i)
        pagePat = r'?start=' + num + '&filter='
        urL = url+pagePat
        urlList.append(urL)
    return urlList


if __name__ == '__main__':
    url = r"https://movie.douban.com/top250"
    path = r"E:\Py\paichong\doubanmovie\\"
    listURL = page(url)
    resp(listURL, path)

















