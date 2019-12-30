# -*- coding: utf-8 -*-
import re
import scrapy


class XpcSpider(scrapy.Spider):
    name = 'xpc'
    allowed_domains = ['xinpianchang.com']
    # start_urls = ['http://xinpianchang.com/']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']

    def parse(self, response):
        video_urls = response.xpath(
            '//div[contains(@class,"channel-con")]/ul[@class="video-list"]/li/@data-articleid').getall()
        video_urls = list(map(lambda x: 'https://www.xinpianchang.com/a' + x, video_urls))
        for video_url in video_urls:
            yield response.follow(video_url, callback=self.parse_post)
            break

        # 自动爬取下一页
        # next_page = response.xpath('//div[@class="page-wrap"]/div[@class="page"]/a[@title="下一页"]/@href').get()
        # if next_page:
        #     next_page = 'https://www.xinpianchang.com/' + next_page
        #     yield response.follow(url=next_page, callback=self.parse)

    def parse_post(self, response):
        # print(response.url)
        post = {}
        # post['video_name'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        cates = response.xpath('//span[contains(@class,"cate")][1]//text()').getall()
        print('=' * 60)
        # cate = list(map(lambda x:re.sub(r'\s|\t',"",x),cates))
        # for index,value in enumerate(cate):
        #     if not value:
        #         cate.pop(index)
        # print(cate)
        print(re.sub(r'\s|\t', '', "".join(cates)))
        print('=' * 60)
