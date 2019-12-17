# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ActicleSpiderItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/p/0a1397ce61ad']
    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="_1RuRku"]/text()').extract_first()
        author = response.xpath('//span[@class="_22gUMi"]/text()').extract_first()
        content = response.xpath('//article/p').extract()
        url = response.url
        url1 = url.split('?')[0]
        article_id = url1.split('/')[-1]
        item = ActicleSpiderItem(title=title, author=author, content=content, origin_url=url, article_id=article_id)
        yield item
