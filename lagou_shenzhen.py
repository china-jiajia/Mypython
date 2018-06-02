import json
import math
import time
import pandas as pd
import requests


url = r'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36",
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Host":"www.lagou.com",
    "Origin":"https://www.lagou.com",
    "Referer":"https://www.lagou.com/jobs/list_python?px=default&city=%E5%B9%BF%E5%B7%9E",
    "Cookie":"JSESSIONID=ABAAABAABEEAAJAED90BA4E80FADBE9F613E7A3EC91067E; _ga=GA1.2.1013282376.1527477899; user_trace_token=20180528112458-b2b32f84-6226-11e8-ad57-525400f775ce; LGUID=20180528112458-b2b3338b-6226-11e8-ad57-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527346927,1527406449,1527423846,1527477899; _gid=GA1.2.1184022975.1527477899; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527487349; LGSID=20180528140228-b38fe5f2-623c-11e8-ad79-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Ddefault%26city%3D%25E5%25B9%25BF%25E5%25B7%259E; TG-TRACK-CODE=index_search; _gat=1; LGRID=20180528141611-9e278316-623e-11e8-ad7c-525400f775ce; SEARCH_ID=42c704951afa48b5944a3dd0f820373d"
}

data = {
    "first":True,
    "pn":1,
    "kd":"python"
}

#json数据爬取
def dataJson(url,headers,data):
    #发起请求（POST）
    req = requests.post(url, data = data, headers = headers)
    #返回并解析请求结果
    response = req.text
    #转换成json格式
    htmlJson = json.loads(response)
    #返回json格式数据
    return htmlJson

#岗位数量和页数
def positonCount(htmlJson):
    # 筛选所需数据
    totalCount = htmlJson["content"]["positionResult"]["totalCount"]
    #每页显示15个岗位(向上取整)
    page = math.ceil((totalCount)/15)
    # 拉勾网最多显示30页结果
    if page > 30:
        return 30
    else:
        return (totalCount,page)

#json数据筛选
def selectData(htmlJson):
    #筛选出岗位详细信息
    jobList = htmlJson["content"]["positionResult"]["result"]
    #创建工作信息列表(外表)
    jobinfoList = []
    #遍历，找出数据
    for jobDict in jobList:
        #创建工作信息列表(内表)
        jobinfo = []
        # 岗位名称
        jobinfo.append(jobDict['positionName'])
        #公司名称
        jobinfo.append(jobDict['companyFullName'])
        #公司性质
        jobinfo.append(jobDict['financeStage'])
        #公司规模
        jobinfo.append(jobDict['companySize'])
        #行业领域
        jobinfo.append(jobDict['industryField'])
        # 办公地点（所处地区）
        jobinfo.append(jobDict['district'])
        #岗位标签
        positionLables = jobDict['positionLables']
        ret1 = ""
        for positionLable in positionLables:
            ret1 += positionLable + "；"
        jobinfo.append(ret1)
        #学历要求
        jobinfo.append(jobDict['education'])
        #工作经验
        jobinfo.append(jobDict['workYear'])
        #工资
        jobinfo.append(jobDict['salary'])
        #待遇
        jobinfo.append(jobDict['positionAdvantage'])
        #公司福利
        companyLabelList = jobDict['companyLabelList']
        ret2 = ""
        for companyLabel in companyLabelList:
            ret2 += companyLabel + "；"
        jobinfo.append(ret2)
        #岗位类型
        jobinfo.append(jobDict['firstType'])
        #发布时间
        jobinfo.append(jobDict['createTime'])
        #添加都岗位信息列表
        jobinfoList.append(jobinfo)
        #间隔时间为30s，防止访问过于频繁
        time.sleep(30)
    return jobinfoList


def main():
    #获取json的页面，返回json格式数据
    htmlJson = dataJson(url, headers, data)
    #找出岗位数量以及页数
    pageTurple = positonCount(htmlJson)
    #岗位列表
    posiList = []
    for i in range(1,pageTurple[1]):
        #页码
        data["pn"] = i
        #再次请求——返回数据
        htmlJson = dataJson(url, headers, data)
        #筛选所需数据
        jobinfoList = selectData(htmlJson)
        #添加到岗位列表
        posiList += jobinfoList
        print("一共%d个岗位，已下载%d页" %(pageTurple[0],i))

    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=posiList,columns=["岗位名称","公司名称","公司性质","公司规模","行业领域",
                                             "办公地点(深圳市)","岗位标签","学历要求","工作经验","工资",
                                             "待遇","公司福利","岗位类型","发布时间"])
    # 数据存入csv文件
    df.to_csv('job_sz_csv',index=False)
    print('已保存文件')

if __name__ == '__main__':
    main()




















































