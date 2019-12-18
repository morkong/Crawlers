# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#import json
import mysql.connector
from scrapy import item


class ShengouPipeline(object):
    # 仅仅输出到控制台
    # def process_item(self, item, spider):
    #     print(item['xh'],'  ',item['sgdm'],'  ',item['zqdm'],'  ',item['name'],'  ',item['wsfxr'],'  ',item['ssr'],
    #     '  ',item['fxl'],'  ',item['wsfxl'],'  ',item['sgsx'],'  ',item['fxj'],'  ',item['syl'],'  ',item['zql'])

    # 将数据写到json文件中
    # 定义构造器, 初始化要写入的文件
    # def __init__(self):
    #     self.json_file =open("table_info.json","wb+")
    #     self.json_file.write('\n'.encode("utf-8"))
    # #重写close_spider 回调方法，用于关闭文件
    # def close_spider(self,spider):
    #     print('--------关闭文件----------')
    #     #后退两个字符，也就是去掉最后一条记录之后的换行街和逗号
    #     self.json_file.seek(-2,1)
    #     self.json_file.write('\n'.encode("utf-8"))
    #     self.json_file.close()
    # def process_item(self,item,spider):
    #     text = json.dumps(dict(item),ensure_ascii = False)+",\n"
    #     self.json_file.write(text.encode("utf-8"))



    # 将数据写入mysql数据库
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost', user='root', database='stocks', port='3306', password='123456',
                use_unicode=True)
            self.cur = self.conn.cursor()
        except Exception as  e:
            print(e)
    # 重写close_spider 回调方法，用于关闭数据库
    def close_spider(self, spider):
        try:
            print('--------关闭数据库资源----------')
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except Exception as  e:
            print(e)
    def process_item(self, item, spider):
        # 1.Python 'list' cannot be converted to a MySQL type
        # self.cur.execute("insert into info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        #                  (item['xh'],item['sgdm'],item['zqdm'],item['name'],item['wsfxr'],item['ssr'],
        #                   item['fxl'],item['wsfxl'],item['sgsx'],item['fxj'],item['syl'],item['zql']))

        # 2.ok
        try:
            values = [item['xh'][0], item['sgdm'][0], item['zqdm'][0], item['name'][0], item['wsfxr'][0], item['ssr'][0],
                      item['fxl'][0],
                      item['wsfxl'][0], item['sgsx'][0], item['fxj'][0], item['syl'][0], item['zql'][0]]
            self.cur.execute("insert into info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
            self.conn.commit()
            print('正在插入数据')
        except Exception as  e:
            print(e)

class StockListPipeline(object):
    # def process_item(self, item, spider):
    #     print(item['name'],item['code'],item['region'])

    # 将数据写入mysql数据库
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost', user='root', database='stocks', port='3306', password='123456',
                use_unicode=True)
            self.cur = self.conn.cursor()
        except Exception as  e:
            print(e)
    # 重写close_spider 回调方法，用于关闭数据库
    def close_spider(self, spider):
        try:
            print('--------关闭数据库资源----------')
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except Exception as  e:
            print(e)
    def process_item(self, item, spider):
        namestr = item['name'][0]
        s = namestr.split('(')
        namestr = s[0]
        regionstr = item['region'][0]
        if regionstr.find('sh') > 0:
            regionstr = 'sh'
        elif regionstr.find('sz') > 0:
            regionstr = 'sz'
        else:
            regionstr = '0'

        values = [namestr, item['code'][0], regionstr]
        try:
            self.cur.execute("insert into stock_code values (%s,%s,%s)", values)
            self.conn.commit()
            print('正在插入数据')
        except Exception as  e:
            print(e)