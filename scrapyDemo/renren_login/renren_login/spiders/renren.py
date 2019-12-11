# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    #覆盖原先start_requests方法
    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        data = {
            'email': '18159661261',
            'password': '476310982zhy'
        }
        #发送post的表单请求
        yield scrapy.FormRequest(url, formdata=data, callback=self.parse_page)

    def parse_page(self, response):
        print(response.text)
