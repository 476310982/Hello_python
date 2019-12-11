# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=1&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=1&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback="parse_item", follow=False),
    )

    def parse_item(self, response):
        title = response.xpath('//div/h1[@class="ph"]/text()').extract_first()
        author_p = response.xpath('//p[@class="authors"]')
        author = author_p.xpath('.//a/text()').extract_first()
        pub_time = author_p.xpath('.//span/text()').extract_first()
        article_context = response.xpath('//td[@id="article_content"]').extract()
        article_context = "".join(article_context).strip().replace('\r','').replace('\n','')
        print('='*20)
        # print(title, author, pub_time)
        # print(article_context)
        print('='*20)
        item = WxappItem(title=title,author=author,pub_time=pub_time,article_context=article_context)
        yield item
