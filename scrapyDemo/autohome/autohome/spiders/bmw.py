# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from autohome.items import AutohomeItem
import re


class BmdSpider(CrawlSpider):
    name = 'bmw'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    pattern = r'https:.+/(.*?)auto.+'
    cate = ""

    # 定义元组要最后面要加个“，”
    rules = {
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.html"), callback="parse_page",
             follow=True),
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65-.+.html"), callback="parse_img",
             follow=True),
        # Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65\.html"), callback="parse_page", follow=True),

    }

    def parse_page(self, response):
        categories = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]')[1:]
        category = categories.xpath('./a[1]/text()').extract()
        page_urls = categories.xpath('./a[1]/@href').extract()
        page_urls = list(map(lambda x: response.urljoin(x), page_urls))
        for cate, url in zip(category, page_urls):
            # print(cate,url)
            yield scrapy.Request(url=url, callback=self.parse_img, meta={'category': cate, 'url': url})

    def parse_img(self, response):
        # print(response.meta)
        if 'category' in response.meta:
            self.cate = response.meta.get('category')
            # print('='*30)
            # print(self.cate)
            img_urls = response.xpath('//div[@class="uibox"]//div[contains(@class,"uibox-con")]//img/@src').extract()
            img_urls = list(map(lambda url: response.urljoin(url) if not url.startswith('https') else url, img_urls))
            img_urls = list(map(
                lambda url: url.replace(re.findall(pattern=self.pattern, string=url)[0], '') if re.findall(
                    pattern=self.pattern, string=url) else url, img_urls))
            item = AutohomeItem(category=self.cate, image_urls=img_urls)
            yield item
        next_page = response.xpath('//div[@class="page"]/a[@class="page-item-next"]/@href').extract()
        if next_page is not None:
            next_page_url = response.urljoin(next_page[0])
            yield scrapy.Request(url=next_page_url, callback=self.parse_img, meta={'category': self.cate, 'url': next_page_url})


    def test_parse(self, response):
        uiboxs = response.xpath('//div[@class="uibox"]')[1:]
        # print(uibox)
        for uibox in uiboxs:
            category = uibox.xpath('.//div[@class="uibox-title"]/a/text()').extract_first()
            urls = uibox.xpath('.//ul/li/a/img/@src').extract()
            urls = list(map(lambda url: response.urljoin(url), urls))
            item = AutohomeItem(category=category, image_urls=urls)
            yield item
