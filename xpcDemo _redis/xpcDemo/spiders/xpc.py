# -*- coding: utf-8 -*-
import re
import json
import string
import random
import scrapy
from scrapy import Request
from xpcDemo.items import videoItem, commentItem, creatorItem, crItem


# 过滤数字中的逗号
def delComma(str):
    return "".join(str.split(","))


# 生成随机的26位id
def gen_sessionId():
    return ''.join(random.choices(string.digits + string.ascii_lowercase, k=26))


# 判断是否为空 不为空则去掉头尾的空字符串
def strip(str):
    if (not str):
        return '暂无描述'
    return str.strip()


cookie = dict(Authorization='A422D63E0D737A03D0D73740AA0D737903D0D7376329177E3CDE')


class XpcSpider(scrapy.Spider):
    name = 'xpc'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    # start_urls = ['http://xinpianchang.com/']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']
    url = 'https://www.xinpianchang.com'
    page_count = 0

    def parse(self, response):
        print('=' * 60)
        print('开始爬取...')
        exUrl = 'https://www.xinpianchang.com/a%s?from=ArticleList'
        ul = response.xpath('//div[@class="channel-con"]/ul[@class="video-list"]/li')
        # urls = list(map(lambda x:exUrl % x,videoUrls))

        # 针对网页的反扒机制,更新id
        self.page_count += 1
        if self.page_count >= 50:
            cookie.update(PHPSESSID=gen_sessionId())
            self.page_count = 0

        for li in ul:
            url = li.xpath('./@data-articleid').get()
            thumbnail = li.xpath('.//img[@class="lazy-img"]/@_src').get()
            request = response.follow(exUrl % url, callback=self.parse_post)
            request.meta['thumbnail'] = thumbnail
            request.meta['pid'] = url
            yield request
        pages = response.xpath('//div[@class="page"]/a/@href').getall()
        pages = list(map(lambda x: self.url + x, pages))
        for page in pages:
            yield response.follow(page, callback=self.parse, cookies=cookie)

    def parse_post(self, response):
        pid = response.meta['pid']
        thumbnail = response.meta['thumbnail']
        post = videoItem()
        post['pid'] = pid
        post['thumbnail'] = thumbnail
        # 获取标题
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        # 获取视频类别
        categories = response.xpath(
            '//div[contains(@class,"filmplay-intro")]/span[contains(@class,"cate")]//text()').getall()
        post['cate'] = ''.join([category.strip() for category in categories])
        post['created_at'] = response.xpath(
            '//div[contains(@class,"filmplay-intro")]/span[contains(@class,"update-time")]//text()').get()
        post['play_counts'] = delComma(response.xpath('//div[contains(@class,"filmplay-data")]/div/i/text()').get())
        post['like_counts'] = delComma(response.xpath(
            '//div[contains(@class,"filmplay-data")]/div//span[contains(@class,"like-counts")]/text()').get())
        post['descr'] = strip(
            response.xpath('//div[contains(@class,"filmplay-info-desc")]/p[contains(@class,"desc")]/text()').get())
        vid = re.findall('vid: \"(\w+)\",', response.text)[0]
        exUrl = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web'
        # 获取视频信息
        request = Request(exUrl % vid, callback=self.parse_video)
        request.meta['post'] = post
        yield request

        # 获取评论信息
        commentsUrl = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=1&per_page=24'
        request = Request(commentsUrl % pid, callback=self.parse_comments)
        yield request

        # 获取视频创作者信息
        creators = response.xpath('//div[contains(@class,"filmplay-creator ")]/ul[contains(@class,"creator-list")]/li')
        for c in creators:
            curl = c.xpath('./div[@class="creator-info"]/a/@href').get()
            cid = c.xpath('./a/@data-userid').get()
            request = Request(self.url + curl, callback=self.parse_composer)
            request.meta['cid'] = cid
            request.meta['dont_merge_cookies'] = True
            yield request

            cr = crItem()
            cr['pcid'] ='%s_%s' %(cid,pid)
            cr['cid'] = cid
            cr['pid'] = pid
            cr['role'] = c.xpath('.//span[contains(@class,"roles")]/text()').get()
            yield cr

    def parse_video(self, response):
        post = response.meta['post']
        result = json.loads(response.text)
        video = result['data']['resource']['default']['url']
        post['video'] = video if video else None
        post['cover'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        # print(post)
        # print(isinstance(post,videoItem))
        yield post

    def parse_comments(self, response):
        result = json.loads(response.text)
        commenter = commentItem()
        comments = result['data']['list']
        for comment in comments:
            commenter['uname'] = comment['userInfo']['username']
            commenter['commentId'] = comment['id']
            commenter['pid'] = comment['resource_id']
            commenter['avatar'] = comment['userInfo']['avatar']
            commenter['content'] = strip(comment['content'])
            commenter['created_at'] = comment['addtime']
            commenter['like_counts'] = comment['count_approve']
            try:
                if comment['referer']:
                    commenter['referer'] = comment['referer']['id']
            except KeyError:
                commenter['referer'] = None
            yield commenter
        nextUrl = result['data']['next_page_url']
        if nextUrl:
            request = response.follow('https://app.xinpianchang.com%s' % nextUrl, callback=self.parse_comments)
            yield request

    def parse_composer(self, response):
        composer = creatorItem()
        composer['cid'] = response.meta['cid']
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer['banner'] = re.findall('background-image:url\((.+?)\)', banner)[0]
        composer['name'] = strip(response.xpath('//p[contains(@class,"creator-name")]/text()').get())
        composer['intro'] = strip(response.xpath('//p[contains(@class,"creator-desc")]/text()').get())
        composer['like_counts'] = delComma(response.xpath('//span[contains(@class,"like-counts")]/text()').get())
        composer['fans_counts'] = delComma(response.xpath('//span[contains(@class,"fans-counts")]/text()').get())
        composer['follow_counts'] = delComma(response.xpath('//span[@class="follow-wrap"]/span[last()]/text()').get())
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/following-sibling::span[1]/text()').get()
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]/following-sibling::span[1]/text()').get()
        yield composer
