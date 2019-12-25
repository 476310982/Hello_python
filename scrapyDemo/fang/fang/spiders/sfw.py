# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem, EsfHouseItem


def newhouse(url):
    parts = url.split('.')
    parts.insert(1, 'newhouse')
    return ".".join(parts) + 'house/s'


def esfhouse(url):
    if 'esf' in url:
        return url
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

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        divs = response.xpath('//div[@class="nhouse_list"]//ul/li//div[@class="nlc_details"]')
        for div in divs:
            name = div.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
            rooms = div.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            rooms = list(filter(lambda x: x.endswith('居'), rooms))
            if not rooms:
                rooms = '未知'
            area = "".join(div.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            area = re.sub(r"\s|－|\/", "", area)
            if area == '':
                area = '未知'
            address = re.sub(r'\[.*\]', "", "".join(div.xpath('.//div[@class="address"]/a/@title').getall()))
            district = "".join(div.xpath('.//div[@class="address"]/a//text()').getall())
            district = re.findall(r".*\[(.+)\].*", district)
            if not district:
                district = '未知'
            else:
                district = district[0]
            sale = div.xpath('//div[contains(@class,"fangyuan")]/span/text()').get()
            price = re.sub(r"\s|广告", "", "".join(div.xpath('.//div[@class="nhouse_price"]//text()').getall()))
            origin_url = div.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            if not origin_url.startswith('https:'):
                origin_url = 'https:' + origin_url
            nitem = NewHouseItem(province=province, city=city, name=name, rooms=rooms, area=area, address=address,
                                 district=district, sale=sale, price=price, origin_url=origin_url)
            yield nitem
        next_url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse,
                                 meta={'info': (province, city)})

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        divs = response.xpath('//div[contains(@class,"shop_list")]/dl[not(@dataflag="bgcomare")]')
        for div in divs:
            name = div.xpath('./dd/p[@class="add_shop"]/a/@title').get()
            infos = div.xpath('./dd/p[contains(@class,"tel_shop")]/text()').getall()
            # print('='*60)
            infos = list(map(lambda x: re.sub(r'\s', "", x), infos))
            rooms, area, floor, toward, year = '未知', '未知', '未知', '未知', '未知'
            for info in infos:
                if ('厅' or '栋' or '室') in info:
                    rooms = info
                elif ('㎡' or '呎') in info:
                    area = info
                elif '层' in info:
                    floor = info
                elif '向' in info:
                    toward = info
                elif '年' in info:
                    year = info.replace('建', '')
            address = div.xpath('./dd/p[contains(@class,"add_shop")]/span/text()').get()
            # price = re.sub(r"\s", "", "".join(div.xpath('./dd[@class="price_right"]/span[1]').getall()))
            price = "".join(div.xpath('./dd[@class="price_right"]/span[1]//text()').getall())
            # print(price)
            unit = div.xpath('./dd[@class="price_right"]/span[2]/text()').get()
            url = div.xpath('./dd/h4/a/@href').get()
            if not url.startswith('https:'):
                url = response.url + url
            # print(url)
            esfItem = EsfHouseItem(province=province, city=city, name=name, area=area, rooms=rooms, floor=floor,
                                   toward=toward,
                                   year=year, address=address, price=price, unit=unit, origin_url=url)
            yield esfItem
        next_url = response.xpath('//div[@class="page_al"]/p[1]/a/@href').get()

        if next_url:
            if not next_url.startswith('https:'):
                next_url = response.url + next_url
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,
                                 meta={'info': (province, city)})
