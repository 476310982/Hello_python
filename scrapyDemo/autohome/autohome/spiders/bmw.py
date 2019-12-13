# -*- coding: utf-8 -*-
import scrapy

from autohome.items import AutohomeItem


class BmdSpider(scrapy.Spider):
    name = 'bmw'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    head_url = 'https://car.autohome.com.cn'

    def parse(self, response):
        uiboxs = response.xpath('//div[@class="uibox"]')[1:]
        # print(uibox)
        for uibox in uiboxs:
            category = uibox.xpath('.//div[@class="uibox-title"]/a/text()').extract_first()
            urls = uibox.xpath('.//ul/li/a/img/@src').extract()
            urls = list(map(lambda url: response.urljoin(url), urls))
            item = AutohomeItem(category=category, image_urls=urls)
            yield item
