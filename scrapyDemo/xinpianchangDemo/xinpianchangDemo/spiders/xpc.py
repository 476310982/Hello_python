# -*- coding: utf-8 -*-
import re
import json
from xinpianchangDemo.items import CommentsItem, VideoInfoItem
from scrapy import Request
import scrapy


# 清洗抓取的cate数据
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


cookie = dict(
    Authorization='F5ED63BD7E6A7C1697E6A742FE7E6A78D847E6A7355AD4DFCB22')


class XpcSpider(scrapy.Spider):
    name = 'xpc'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    # start_urls = ['http://xinpianchang.com/']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']

    def parse(self, response):
        # 获得文章id
        video_urls = response.xpath(
            '//div[contains(@class,"channel-con")]/ul[@class="video-list"]/li/@data-articleid').getall()
        url = 'https://www.xinpianchang.com/a%s'
        for video_url in video_urls:
            request = response.follow(url % video_url, callback=self.parse_post)
            request.meta['pid'] = video_url
            # yield request

        # 自动爬取下一页
        next_page = response.xpath('//div[@class="page-wrap"]/div[@class="page"]/a[@title="下一页"]/@href').get()
        if next_page:
            next_page = 'https://www.xinpianchang.com/' + next_page
            yield response.follow(url=next_page, callback=self.parse,cookies=cookie)

    def parse_post(self, response):
        pid = response.meta['pid']
        post = VideoInfoItem()
        post['pid'] = pid
        # 获取标题
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        cates = response.xpath('//span[contains(@class,"cate")]//text()').getall()
        # cates = "".join([c.strip() for c in cates])
        # print("".join([c.strip() for c in cates]))
        res = cate_fun(cates)
        # 获取视频类别
        post['category'] = res
        # 获取视频发布时间
        post['update_time'] = response.xpath('//span[contains(@class,"update-time")]/i/text()').get()
        # 获取视频点赞数量
        post['like_counts'] = response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get()
        # 获取播放量
        post['curplaycounts'] = response.xpath(
            '//div[contains(@class,"filmplay-data-play")]/i/@data-curplaycounts').get()
        # 获取视频简介，部分视频没有简介，所以进行过判断
        post['desc'] = response.xpath('//div[contains(@class,"desc")]/p/text()').get()
        if post['desc']:
            post['desc'] = post['desc'].strip()
        else:
            post['desc'] = '暂无简介'
        # 获取视频标签
        post['tags'] = response.xpath('//div[contains(@class,"filmplay-info-tags")]/div/a/text()').getall()
        creator_info = response.xpath('//div[@class="user-team"]//li/div[@class="creator-info"]')
        creators = creator_info.xpath('.//span[contains(@class,"name")]/text()').getall()
        roles = creator_info.xpath('.//span[contains(@class,"role")]/text()').getall()
        post['creator_info'] = dict(zip(creators, roles))

        # 经过排查，视频的相关信息是通过ajax动态加载出来的，万幸的是保存在了页面源代码内，可以通过正则表达式找出唯一值
        vid = re.findall('vid: \"(\w+)\",', response.text)[0]
        url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web'
        # 此处url超出了爬虫的域名限制，必须将该新域名添加进去
        request = Request(url % vid, callback=self.parse_video)
        # 将已经获得的数据一起携带发送
        request.meta['post'] = post
        yield request

        # 获取视频评论（动态加载）
        # comment_url = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=%d&per_page=24'
        # request = Request(comment_url % (pid, 1), callback=self.parse_comment)
        # request.meta['pid'] = pid
        # request.meta['page'] = 1
        # yield request

    # 获取视频相关信息
    def parse_video(self, response):
        post = response.meta['post']
        # 获得了一个json页面，解析内容
        result = json.loads(response.text)
        post['video_url'] = result['data']['resource']['default']['url']
        post['video_cover'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        yield post

    # 获取评论数据
    def parse_comment(self, response):
        pid = response.meta['pid']
        page = response.meta['page']
        content = json.loads(response.text)
        content_list = content['data']['list']
        if content_list:
            for item in content_list:
                comment = CommentsItem()
                comment['pid'] = pid
                comment['userid'] = item['userid']
                comment['content'] = item['content']
                comment['username'] = item['userInfo']['username']
                # comments.append(comment)
                yield comment
            # 翻页获取下一页评论
            page += 1
            comment_url = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=%d&per_page=24'
            request = Request(comment_url % (pid, page), callback=self.parse_comment)
            request.meta['pid'] = pid
            request.meta['page'] = page
            yield request
