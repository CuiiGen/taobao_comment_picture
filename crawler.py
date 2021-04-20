# -*- coding: utf-8 -*-
import _thread
import json
from logging import info
from os import makedirs, path
from time import time

import requests

REFER_TMALL = 0
REFER_TAOBAO = 1


class crawler:
    def __init__(self, category):
        '''
        构造函数

        @category 表示待爬取商品平台属于淘宝还是天猫，可选REFER_TMALL或REFER_TAOBAO
        '''
        # 类别
        self.__cate = category
        # 基本URL
        self.__url = ['https://rate.tmall.com/list_detail_rate.htm',
                      'https://rate.taobao.com/feedRateList.htm']
        # 配置文件
        conf = {}
        with open('property.json', 'r') as f:
            conf = json.loads(f.read())
        # 查询参数中页码键
        self.__page = 'currentPage'
        # 返回文本末端需要截取长度
        self.__rearlen = 1
        if category == REFER_TAOBAO:
            self.__page = 'currentPageNum'
            self.__rearlen = 2
        # 查询参数
        self.__params = [
            {
                'itemId': conf.get('itemId'),
                'spuId': conf.get('spuId'),
                'sellerId': conf.get('sellerId'),
                'order': 3,
                'append': 0,
                'content': 1,
                'picture': 1,
                'needFold': 0,
                '_ksTS': '%d_0000' % time(),
                'callback': '_'
            },
            {
                'auctionNumId': conf.get('auctionNumId'),
                'userNumId': conf.get('userNumId'),
                'pageSize': 20,
                'rateType': 3,
                'orderType': 'sort_weight',
                'hasSku': False,
                'folded': 0,
                '_ksTS': '%d_0000' % time(),
                'callback': '_'
            }
        ]
        # 请求头
        dictheader = ['https://detail.tmall.com/item.htm',
                      'https://item.taobao.com/item.htm']
        self.__headers = {
            'referer': dictheader[self.__cate],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'cookie': conf.get('cookie')
        }
        # 保存数据列表
        self.__datalist = []
        # 检查img文件是否存在否则创建
        dirs = './img/'
        if not path.exists(dirs):
            makedirs(dirs)

    def __run_page(self, page):
        '''
        子线程中启动运行该函数

        用于多线程爬取第page个页面信息
        '''
        info('page start: %2d' % page)
        self.__params[self.__cate][self.__page] = page
        r = requests.get(
            self.__url[self.__cate], self.__params[self.__cate], headers=self.__headers)
        r.encoding = 'utf-8'
        # 解析结果
        detail = json.loads(r.text[4:len(r.text)-self.__rearlen])
        t = []
        if self.__cate == REFER_TMALL:
            # 天猫
            ratelist = detail.get('rateDetail').get('rateList')
            for i in ratelist:
                t.extend(i.get('pics'))
                # 追加评论
                if i.get('appendComment') is not None:
                    t.extend(
                        i.get('appendComment').get('pics'))
        else:
            # 淘宝
            ratelist = detail.get('comments')
            for i in ratelist:
                t.extend([j.get('url') for j in i.get('photos')])
                if i.get('append') is not None:
                    t.extend([j.get('url')
                              for j in i.get('append').get('photos')])

            ratelist = detail.get('comments')
        # 输出结果
        info('page: %2d \t size: %2d' % (page, len(ratelist)))
        # 更新全局图片列表
        self.__datalist.extend(t)
        # 爬取图片
        _thread.start_new_thread(
            self.__download_multithread, (t, page))

    def run(self):
        '''
        运行爬虫程序
        '''
        page = 1
        self.__params[self.__cate][self.__page] = page
        r = requests.get(
            self.__url[self.__cate], self.__params[self.__cate], headers=self.__headers)
        r.encoding = 'utf-8'
        # 解析结果
        detail = json.loads(r.text[4:len(r.text)-self.__rearlen])
        if self.__cate == REFER_TMALL:
            lastpage = detail.get('rateDetail').get(
                'paginator').get('lastPage')
        else:
            lastpage = int(detail.get('total') / 20) + 1
        # 日志输出
        info('lastPage: %2d' % lastpage)
        for i in range(lastpage):
            _thread.start_new_thread(self.__run_page, (i + 1,))

    def save(self, path):
        '''
        将结果保存在本地

        @path   保存结果路径及文件名
        '''
        # 保存结果到本地
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__datalist, ensure_ascii=False, indent=4))
            f.flush()
        info('file destination: %s' % path)

    def __download_subtread(self, i, j, img_url):
        '''
        子线程中启动运行该函数

        用于多线程爬取第i个页面中所有图片
        '''
        if self.__cate == REFER_TAOBAO:
            r = requests.get('https:' + img_url[:len(img_url) - 12])
        else:
            r = requests.get('http:' + img_url)
        with open('./img/%d_%d.jpg' % (i, j), 'wb') as f:
            f.write(r.content)
            f.flush()

    def __download_multithread(self, sublist, page):
        '''
        子线程中启动运行该函数

        用于在获取某一页面所有图片URL之后开始图片爬取工作
        '''
        for i in range(len(sublist)):
            info('progress: %2d - %d / %d' % (page, i, len(sublist) - 1))
            _thread.start_new_thread(
                self.__download_subtread, (page, i, sublist[i]))
