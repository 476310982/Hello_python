# -*- coding: utf-8 -*-
import re
from scrapy import Request
import scrapy
import json


def cate_fun(cates):
    cates = [i.strip() for i in cates]

    res = []
    for index, value in enumerate(cates):
        if not value:
            cates.pop(index)
    for i in range(len(cates) - 2):
        if re.match('\w+', cates[i]) and cates[i + 1] == '-':
            res.append(cates[i] + '-' + cates[i + 2])
            i = i + 2
        else:
            if cates[i] != '-' and cates[i] != '' and cates[i - 1] != '-':
                res.append(cates[i])
    # res.append(cates[-1])
    return res


class XpcSpider(scrapy.Spider):
    name = 'xpc'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    # start_urls = ['http://xinpianchang.com/']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']

    def parse(self, response):
        video_urls = response.xpath(
            '//div[contains(@class,"channel-con")]/ul[@class="video-list"]/li/@data-articleid').getall()
        video_urls = list(map(lambda x: 'https://www.xinpianchang.com/a' + x, video_urls))
        for video_url in video_urls:
            yield response.follow(video_url, callback=self.parse_post)
            # break

        # 自动爬取下一页
        # next_page = response.xpath('//div[@class="page-wrap"]/div[@class="page"]/a[@title="下一页"]/@href').get()
        # if next_page:
        #     next_page = 'https://www.xinpianchang.com/' + next_page
        #     yield response.follow(url=next_page, callback=self.parse)

    def parse_post(self, response):
        # 保存数据
        post = {}
        # 获取标题
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        cates = response.xpath('//span[contains(@class,"cate")]//text()').getall()
        # cates = "".join([c.strip() for c in cates])
        # print("".join([c.strip() for c in cates]))
        res = cate_fun(cates)
        post['category'] = res
        post['update_time'] = response.xpath('//span[contains(@class,"update-time")]/i/text()').get()
        post['like_counts'] = response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get()
        post['curplaycounts'] = response.xpath(
            '//div[contains(@class,"filmplay-data-play")]/i/@data-curplaycounts').get()
        post['desc'] = response.xpath('//div[contains(@class,"desc")]/p/text()').get()
        if post['desc']:
            post['desc'] = post['desc'].strip()
        else:
            post['desc'] = '暂无简介'
        post['tags'] = response.xpath('//div[contains(@class,"filmplay-info-tags")]/div/a/text()').getall()

        # 经过排查，视频的相关信息是通过ajax动态加载出来的，万幸的是保存在了页面源代码内，可以通过正则表达式找出唯一值
        vid = re.findall('vid: \"(\w+)\",', response.text)[0]
        url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web'
        # 此处url超出了爬虫的域名限制，必须将该新域名添加进去
        request = Request(url % vid, callback=self.parse_video)
        # 将已经获得的数据一起携带发送
        request.meta['post'] = post
        yield request

    def parse_video(self, response):
        post = response.meta['post']
        # 获得了一个json页面，解析内容
        result = json.loads(response.text)
        post['video_url'] = result['data']['resource']['default']['url']
        print(post)
