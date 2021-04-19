# 淘宝/天猫商品评论图片爬虫

> 该程序用于爬取淘宝/天猫电商平台中商品评论中的所有图片并保存自本地。
> 
> iamroot
> 
> 2021年4月19日

## 环境说明

该程序开发环境为`Python 3.8.5 64-bit`，所需第三方库为`requests`，用户可通过命令`pip install requests`进行安装。

## 运行说明

- 正式运行前请保证本地Python开发环境的正确安装与配置；

- 在电脑端浏览器登录淘宝/天猫，打开待爬取商品的评论区，并通过浏览器的检查功能查看评论查询URL及相关请求头信息，详细操作见下图所示；

  <img src="https://github.com/CuiiGen/taobao_comment_picture/raw/main/gif/temp.gif" style="zoom:80%;" />

- 根据上一步操作中查询得到的信息进一步正确修改配置文件`property.json`，其中字段`itemId`、`spuId`和`sellerId`仅用于天猫平台，字段`auctionNumId`和`userNumId`仅用于淘宝平台，`cookie`用于进行身份验证；

- 修改`run.py`中的`main()`函数，主要修改15行中平台类别以及19行文件保存路径，虽有运行即可。

## 类说明

在文件`crawler.py`中定义了爬虫类`crawler`，用户可通过实例化该类进行运行爬虫。其具体方体介绍如下:

- 构造函数。构造函数用于初始化URL、参数、请求头等信息，其输入参数用于判断爬取天猫或者淘宝平台，可选`REFER_TAOBAO`或`REFER_TMALL`；
- `run()`。该函数用于运行爬虫并实时将图片爬取保存在本地`./img/`目录下，文件以`i_j.jpg`格式命名，其中`i`表示页码，`j`表示图片在当前页中的顺序；
- `save(path)`。该函数用于将图片URL信息以文本格式保存在本地，输入参数表示存储目录及文件名，文本信息以json格式保存，文件后缀一般为`.json`，如`./data.json`。