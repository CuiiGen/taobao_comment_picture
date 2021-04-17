# -*- coding: utf-8 -*-
import json
from logging import info
from time import time

import requests


class crawler:
    def __init__(self):
        # 基本URL
        self.url = 'https://rate.tmall.com/list_detail_rate.htm'
        # 配置文件
        conf = {}
        with open('property.json', 'r') as f:
            conf = json.loads(f.read())
        # 查询参数
        self.params = {
            'itemId': conf.get('itemId'),
            'spuId': conf.get('spuId'),
            'sellerId': conf.get('sellerId'),
            'order': '3',
            'append': '0',
            'content': '1',
            'picture': '1',
            'needFold': '0',
            '_ksTS': '%d_0000' % time(),
            'callback': '_'
        }
        # 请求头
        self.headers = {
            'referer': 'https://detail.tmall.com/item.htm',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'cookie': conf.get('cookie')
        }
        self.datalist = []

    def run(self):
        # 循环变量
        page = 1
        # 开始循环
        while True:
            info('current page num: \t%d' % page)
            self.params['currentPage'] = page
            r = requests.get(self.url, self.params, headers=self.headers)
            r.encoding = 'utf-8'
            # 解析结果
            detail = json.loads(r.text[4:len(r.text)-1])
            ratelist = detail.get('rateDetail').get('rateList')
            # 判断结果
            info('page size: \t%d' % len(ratelist))
            if len(ratelist) > 0:
                for i in ratelist:
                    self.datalist.extend(i.get('pics'))
                    # 追加评论
                    if i.get('appendComment') is not None:
                        self.datalist.extend(
                            i.get('appendComment').get('pics'))
                page += 1
            else:
                break

    def save(self, path):
        # 保存结果到本地
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.datalist, ensure_ascii=False, indent=4))
            f.flush()
        info('file destination: %s' % path)

    def download(self):
        # 抓取图片
        for i in range(len(self.datalist)):
            info('progress: %d/%d' % (i, len(self.datalist) - 1))
            r = requests.get('http:' + self.datalist[i])
            with open('./img/%d.jpg' % i, 'wb') as f:
                f.write(r.content)
                f.flush()
