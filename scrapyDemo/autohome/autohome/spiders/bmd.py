# -*- coding: utf-8 -*-
import scrapy

from autohome.items import AutohomeItem


class BmdSpider(scrapy.Spider):
    name = 'bmd'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['http://car.autohome.com.cn/']
    head_url = 'https://car.autohome.com.cn'

    def start_requests(self):
        url = 'https://car.autohome.com.cn/pic/series/65.html'
        yield scrapy.Request(url=url,callback=self.parse_allpage)


    def parse_allpage(self,response):
        self.categroy = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]/a[1]/text()').extract()[1:]
        all_url = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]/a[2]/@href').extract()
        all_url = list(map(lambda x:self.head_url + x,all_url))
        print(self.categroy,all_url)
        for url in all_url:
            yield response.follow(url=url,callback=self.parse)


    def parse(self, response):

        img_urls = response.xpath('//div[contains(@class,"uibox")]/ul/li/a/img/@src').extract()
        for url in img_urls:
            img_name = url.split('__')[-1]
            url = 'https:' + url
            item = AutohomeItem(img_name=img_name,img_url=url)
            yield item



