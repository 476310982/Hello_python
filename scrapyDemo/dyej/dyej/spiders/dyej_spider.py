# -*- coding: utf-8 -*-
import scrapy
from PIL import Image
# import requests
from urllib import request


class DyejSpiderSpider(scrapy.Spider):
    name = 'dyej_spider'
    allowed_domains = ['fj.dyejia.cn']
    start_urls = ['https://fj.dyejia.cn/partysso/index/login.htm?redirect=http%3A%2F%2Ffj.dyejia.cn%2Fpmc']
    head_url = 'https://fj.dyejia.cn/partysso/index/'

    def parse(self, response):
        formdata = {
            'auth': '350521199704041039',
            'passwd': '476310982zhy.'
        }
        img_url = response.xpath('//span/img/@src').extract()[0][1:]
        print(self.head_url + img_url)
        validCode = self.save_validImg(self.head_url + img_url)
        formdata['chkcode'] = validCode
        yield scrapy.FormRequest('https://fj.dyejia.cn/party/',formdata=formdata,callback=self.parse_page)

    def parse_page(self,response):
        # print(response.url)
        if response.url == 'https://fj.dyejia.cn/pmc/index/pmc.htm':
            print('登陆成功')
            url = self.head_url + response.xpath('//div[@id="left"]/div[contains(@class,"index-l-nav")]/div[1]/ul/li[1]/a/@href').extract()[0]
            print(url)
        else:
            print('登陆失败')

    def save_validImg(self, url):
        # 调用方法保存图片
        request.urlretrieve(url=url, filename='validImg.png')
        img = Image.open('validImg.png')
        img.show()
        keyInput = input('请输入验证码：')
        # print('=' * 20)
        # print(keyInput)
        return  keyInput
