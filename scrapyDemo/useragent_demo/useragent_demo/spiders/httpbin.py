# -*- coding: utf-8 -*-
import scrapy
import json

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        UA = json.loads(response.text)['user-agent']
        print('='*60)
        print(UA)
        print('='*60)
        yield scrapy.Request(url=self.start_urls[0],dont_filter=True)

