# -*- coding: utf-8 -*-
import scrapy

from crawlers.items import ShengouItem


class ShengouSpider(scrapy.Spider):
    name = 'shengou'
    allowed_domains = ['quotes.money.163.com']
    start_urls = ['http://quotes.money.163.com/data/ipo/shengou.html']
    custom_settings ={
        'ITEM_PIPELINES' :
            {'crawlers.pipelines.ShengouPipeline': 300}
    }

    def parse(self, response):
        for table_primary in response.xpath('//div[@class="fn_rp_list"]/table/tr'):
            item = ShengouItem()
            # fn_rp_list = table_primary.xpath('./tr')
            item['xh'] = table_primary.xpath('./td[1]/text()').extract()
            item['sgdm'] = table_primary.xpath('./td[2]/text()').extract()
            item['zqdm'] = table_primary.xpath('./td[3]/text()').extract()
            item['name'] = table_primary.xpath('./td[4]/a/text()').extract()
            item['wsfxr'] = table_primary.xpath('./td[5]/text()').extract()
            item['ssr'] = table_primary.xpath('./td[6]/text()').extract()
            item['fxl'] = table_primary.xpath('./td[7]/text()').extract()
            item['wsfxl'] = table_primary.xpath('./td[8]/text()').extract()
            item['sgsx'] = table_primary.xpath('./td[9]/text()').extract()
            item['fxj'] = table_primary.xpath('./td[10]/text()').extract()
            item['syl'] = table_primary.xpath('./td[11]/text()').extract()
            item['zql'] = table_primary.xpath('./td[12]/text()').extract()
            yield item
            # new_links = response.xpath('//a[@class="pages_flip"]/@href').extract()
            new_links = response.xpath('//a[contains(text(), "下一页")]/@href').extract()

            if new_links and len(new_links) > 0:
                new_link = new_links[0]
                yield scrapy.Request("http://quotes.money.163.com" + new_link, callback=self.parse)

