# -*- coding: utf-8 -*-
import scrapy
from crawlers.items import StockListItem

class StockListSpider(scrapy.Spider):
    name = 'stock_list'
    allowed_domains = ['quote.eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/stock_list.html']
    custom_settings = {
        'ITEM_PIPELINES':
            {'crawlers.pipelines.StockListPipeline': 800}
    }
    def parse(self, response):
        for table_primary in response.xpath('//div[@id="quotesearch"]/ul/li'):
            item = StockListItem()
            item['name'] = table_primary.xpath('./a/text()').extract()
            item['code'] = table_primary.xpath('./a/text()').re(r'[(](.*?)[)]')
            item['region'] = table_primary.xpath('./a/@href').extract()

            yield item
