# -*- coding: utf-8 -*-
import scrapy
import re


def newhouse(url):
    parts = url.split('.')
    parts.insert(1, 'newhouse')
    return ".".join(parts) + 'house/s'


def esfhouse(url):
    parts = url.split('.')
    parts.insert(1, 'esf')
    return ".".join(parts)


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        print('开始运行....')
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(contains(@class,"font01"))]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').extract_first()
            province_text = re.sub('\s', '', province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue
            city_td = tds[1]
            city_links = city_td.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').extract_first()
                city_url = city_link.xpath('.//@href').extract_first()
                if 'bj' in city_url:
                    newhouse_url = 'https://newhouse.fang.com'
                    esf_url = 'https://esf.fang.com'
                else:
                    # 构建城市新房链接
                    newhouse_url = newhouse(city_url)
                    # 构建城市二手房链接
                    esf_url = esfhouse(city_url)
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'info': (province, city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': (province, city)})
                # print('省份:%s' % province)
                # print('城市:%s' % city)
                # print('网址:%s' % city_url)
                # print('新房:%s' % newhouse_url)
                # print('二手房:%s' % esf_url)

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        print(province, city)

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        print(province, city)
