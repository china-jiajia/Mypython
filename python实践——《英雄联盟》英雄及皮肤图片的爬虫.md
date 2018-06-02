# python实践——《英雄联盟》英雄及皮肤图片的爬虫

我的博客：https://my.csdn.net/weixin_42108731



刚学python不久，听别人说用python写爬虫可以爬取网站数据，于是在网上搜索了一些资料，无意中在知乎和论坛上看到一些大神分享的关于python爬虫的博文，觉得挺有趣，于是利用最近学的一些python知识自己也写一个，功夫不负有心人，终于给我写出了一个——《英雄联盟》英雄及皮肤图片的爬虫，下面给大家分享一下。

一开始都是先去《英雄联盟》官网找到英雄及皮肤图片的网址：

```
URL = r'http://lol.qq.com/web201310/info-heros.shtml'
```

从上面网址可以看到所有英雄都在，按下F12查看源代码，发现英雄及皮肤图片并没有直接给出，而是隐藏在JS文件中。这时候需要点开Network，找到js窗口，刷新网页，就看到一个champion.js的选项，点击可以看到一个字典——里面就包含了所有英雄的名字（英文）以及对应的编号（如下图）。

![img](https://img-blog.csdn.net/20180501002453263)

但是只有英雄的名字（英文）以及对应的编号并不能找到图片地址，于是回到网页，随便点开一个英雄，跳转页面后发现英雄及皮肤的图片都在，但要下载还需要找到原地址，这是鼠标右击选择“在新标签页中打开”，新的网页才是图片的原地址（如下图）。

![img](https://img-blog.csdn.net/20180501003013695)

图中红色框就是我们需要的图片地址，经过分析知道：每一个英雄及皮肤的地址只有编号不一样（http://ossweb-img.qq.com/images/lol/web201310/skin/big266000.jpg），而该编号有6位，前3位表示英雄，后三位表示皮肤。刚才找到的js文件中恰好有英雄的编号，而皮肤的编码可以自己定义，反正每个英雄皮肤不超过20个，然后组合起来就可以了。

图片地址搞掂都就可以开始写程序了：

第一步：获取js字典

```
def path_js(url_js):
    res_js = requests.get(url_js, verify = False).content
    html_js = res_js.decode("gbk")
    pat_js = r'"keys":(.*?),"data"'
    enc = re.compile(pat_js)
    list_js = enc.findall(html_js)
    dict_js = eval(list_js[0])
    return dict_js
```

第二步：从 js字典中提取到key值生成url列表

```
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
```

第三步：从 js字典中提取到value值生成name列表

```
def name_pic(dict_js, path):
    list_filePath = []
    for name in dict_js.values():
        for i in range(20):
            file_path = path + name + str(i) + '.jpg'
            list_filePath.append(file_path)
    return list_filePath
```

第四步：下载并保存数据

```
def writing(url_list, list_filePath):
    try:
        for i in range(len(url_list)):
            res = requests.get(url_list[i], verify = False).content
            with open(list_filePath[i], "wb") as f:
                f.write(res)

    except Exception as e:
        print("下载图片出错,%s" %(e))
        return False
```

执行主程序：

```
if __name__ == '__main__':
    url_js = r'http://lol.qq.com/biz/hero/champion.js'
    path = r'E:\Py\paichong\LOLpic\\'
    dict_js = path_js(url_js)
    url_list = path_url(dict_js)
    list_filePath = name_pic(dict_js, path)
    writing(url_list, list_filePath)
```

运行后会在控制台打印出每一张图片的网址：

![img](https://img-blog.csdn.net/20180501004444496)

在文件夹中可以看到图片已经下载好：

![img](https://img-blog.csdn.net/20180501004659135)

以上就是我的分享，如果有什么不足之处请指出，多交流，谢谢！

如果喜欢，请关注我的博客：https://my.csdn.net/weixin_42108731