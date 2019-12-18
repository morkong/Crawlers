# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class ShengouItem(scrapy.Item):
    xh = scrapy.Field()  # 序号
    sgdm = scrapy.Field()  # 申购代码
    zqdm = scrapy.Field()  # 证券代码
    name = scrapy.Field()  # 证券简称
    wsfxr = scrapy.Field()  # 网上发行日
    ssr = scrapy.Field()  # 上市日
    fxl = scrapy.Field()  # 发行量
    wsfxl = scrapy.Field()  # 网上发行量
    sgsx = scrapy.Field()  # 申购上限
    fxj = scrapy.Field()  # 发行价
    syl = scrapy.Field()  # 市盈率
    zql = scrapy.Field()  # 中签率
class StockListItem(scrapy.Item):
    name = scrapy.Field() #基金名称
    code = scrapy.Field() #基金代码
    region = scrapy.Field() #区域（上海sh,深圳sz）
