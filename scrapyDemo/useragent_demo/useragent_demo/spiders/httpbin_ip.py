# -*- coding: utf-8 -*-
import scrapy


class HttpbinIpSpider(scrapy.Spider):
    name = 'httpbin_ip'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print(response.meta['proxy'])
        yield scrapy.Request(url=self.start_urls[0],dont_filter=True)
