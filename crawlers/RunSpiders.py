#！/user/bin/env python
#- *- coding:utf-8 -*-
from scrapy import cmdline
def run_shengou():
    cmdline.execute(['scrapy','crawl','shengou'])
    print('shengou run completed')
def run_stock_list():
    cmdline.execute(['scrapy','crawl','stock_list'])
    print('stock_list run completed')

if __name__ == '__main__':
   i = input("输入数字 1: 运行shengou\n输入数字 2 : 运行stock_list\n")
   if i == '1':
       print(run_shengou())
   elif i == '2':
       print(run_stock_list())