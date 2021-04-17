# -*- coding: utf-8 -*-
import logging

from crawler import crawler

# 配置logging模块
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s'
)


def main():
    c = crawler()
    c.run()
    c.save('./data.json')


if __name__ == '__main__':
    main()
