# -*- coding: utf-8 -*-
import logging
from time import sleep

import crawler

# 配置logging模块
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s'
)


def main():
    c = crawler.crawler(crawler.REFER_TAOBAO)
    c.run()
    # # 等待进程结束
    sleep(10)
    c.save('./data.json')


if __name__ == '__main__':
    main()
