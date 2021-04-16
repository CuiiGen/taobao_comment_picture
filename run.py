# -*- coding: utf-8 -*-
import json

import requests


def main():
    # 基本URL
    url = 'https://rate.tmall.com/list_detail_rate.htm'
    # 配置文件
    conf = {}
    with open('property.json', 'r') as f:
        conf = json.loads(f.read())
    # 查询参数
    params = {
        'itemId': conf.get('itemId'),
        'spuId': conf.get('spuId'),
        'sellerId': conf.get('sellerId'),
        'order': '3',
        'append': '0',
        'content': '1',
        'picture': '1',
        'needFold': '0',
        '_ksTS': ' 1618554248318_4050',
        'callback': '_'
    }
    # 请求头
    headers = {
        'referer': 'https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w15914064-15567552165.71.69ff5f3bbwxFUa&id=640860381255&scene=taobao_shop',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'cookie': conf.get('cookie')
    }
    # 结果列表
    datalist = []
    page = 1
    while True:
        params['currentPage'] = page
        r = requests.get(url, params, headers=headers)
        r.encoding = 'utf-8'
        # 解析结果
        detail = json.loads(r.text[4:len(r.text)-1])
        ratelist = detail.get('rateDetail').get('rateList')
        # 判断结果
        if len(ratelist) > 0:
            for i in ratelist:
                datalist.extend(i.get('pics'))
                # 追加评论
                if i.get('appendComment') is not None:
                    datalist.extend(i.get('appendComment').get('pics'))
            page += 1
        else:
            break
    # 保存结果到本地
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(datalist, ensure_ascii=False, indent=4))
        f.flush()


if __name__ == '__main__':
    main()
