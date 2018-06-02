# python实践3——利用爬虫爬取“广州各大行业微信群二维码信息”及存入数据到MySQL数据库

本次以“广州各大行业微信群二维码信息”为例，利用爬虫进行信息“爬取”，并存入数据库，方便后面数据分析处理，以及调用。话不多说，直接上代码：

```
import pymysql
import requests
import re


def download(urlList):

    #连接MySQL
    conn = pymysql.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        password = '123456',
        database = 'pachong',
        charset = 'utf8'
    )

    #获取数据库游标
    cursor = conn.cursor()

    #创建表格
    cursor.execute("create table t_QR(id INT PRIMARY KEY auto_increment NOT NULL,name VARCHAR(50),erweima VARCHAR(230),weixinhao VARCHAR(60),industry VARCHAR(60))")

    for urlpath in urlList:
        #发起网络请求并下载资源（网页源代码）
        res = requests.get(urlpath)
        html = res.text

        # 筛选数据（正则表达式）[群名，二维码图片地址，微信号，行位分类]
        nameGroup = r'alt="(.*?)">'
        erweima = r'<img src="(.*?)">'
        weixinhao = r'<p class="wxNum c888 ellips">\s*(.*?)\s*</p>'
        industry = r'</span>\s*(.*?)\s*</p>'
        name_group = re.compile(nameGroup)
        erweima_img = re.compile(erweima)
        weixin_hao = re.compile(weixinhao)
        industry_name = re.compile(industry)
        name_list = name_group.findall(html)
        erweima_list = erweima_img.findall(html)
        weixinhao_list = weixin_hao.findall(html)
        industry_list = industry_name.findall(html)

        # 数据再处理，获得最终需要数据
        name_list1 = name_list[2:-1]
        erweima_list1 = []
        for i in range(3,len(erweima_list)-1,2):
            erweima_list1.append(erweima_list[i])
        industry_list1 = []
        for j in range(1,len(industry_list),2):
            industry_list1.append(industry_list[j])

        #将爬取的数据存入数据库MySQL中
        for k in range(len(name_list1)):
            cursor.execute('insert into t_QR(name,erweima,weixinhao,industry) VALUES("%s","%s","%s","%s")' %(name_list1[k],erweima_list1[k],weixinhao_list[k],industry_list1[k]))

    #获取游标中结果数据
    cursor.fetchall()

    #结果提交
    conn.commit()
    print("结果已提交")

    #断开连接
    conn.close()


#生成1-442页网址的列表（字符串的拼接）
def url_list(url):
    urlList = []
    # 因442页数据太多，先爬取5页看看效果
    for i in range(5):
        urlPath = url + '&p=' + str(i)
        urlList.append(urlPath)
    return urlList


if __name__ == '__main__':
    url = r'https://www.weixinqun.com/group?c=440100&m=1'
    urlList = url_list(url)
    download(urlList)

```

结果图如下：

其中数据库保存了二维码的地址，只要读取地址，就可以找到相应的二维码。

![](E:\Py\py_mysql\t_qr.png)