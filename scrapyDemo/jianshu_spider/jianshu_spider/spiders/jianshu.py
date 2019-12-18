# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ActicleSpiderItem
import re


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com']
    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        # 匹配阅读量跟文章字数
        pattern = '\d'
        # 提取response中的目标数据
        title = response.xpath('//h1[@class="_1RuRku"]/text()').extract_first()
        author = response.xpath('//span[@class="_22gUMi"]/text()').extract_first()
        content = response.xpath('//article/p').extract()[0]
        url = response.url
        url1 = url.split('?')[0]
        article_id = url1.split('/')[-1]
        spans = response.xpath('//div[@class="s-dsoj"]/span/text()').getall()
        if len(spans) == 3:
            word_count = int("".join(re.findall(pattern, spans[1])))
            read_count = int("".join(re.findall(pattern, spans[2])))
        else:
            word_count = int("".join(re.findall(pattern, spans[0])))
            read_count = int("".join(re.findall(pattern, spans[1])))
        # 将列表转化为逗号分隔的拼接字符串
        subjects = ",".join(response.xpath('//div[@class="_2Nttfz"]/a/span/text()').getall())
        # 生成item对象，将发送给pipeline处理
        item = ActicleSpiderItem(title=title, author=author, content=content, origin_url=url, article_id=article_id,
                                 read_count=read_count, word_count=word_count, subjects=subjects)
        yield item
