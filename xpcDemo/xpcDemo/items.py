# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class videoItem(scrapy.Item):
    # define the fields for your item here like:
    table_name = 'video'
    pid = scrapy.Field()
    title = scrapy.Field()
    cate = scrapy.Field()
    created_at = scrapy.Field()
    play_counts = scrapy.Field()
    like_counts = scrapy.Field()
    descr = scrapy.Field()
    video = scrapy.Field()
    cover = scrapy.Field()
    thumbnail = scrapy.Field()
    duration = scrapy.Field()

class commentItem(scrapy.Item):
    # define the fields for your item here like:
    table_name = 'comment'
    pid = scrapy.Field()
    uname = scrapy.Field()
    commentId = scrapy.Field()
    avatar = scrapy.Field()
    created_at = scrapy.Field()
    like_counts = scrapy.Field()
    referer = scrapy.Field()
    userId = scrapy.Field()
    content = scrapy.Field()



class creatorItem(scrapy.Item):
    # define the fields for your item here like:
    table_name = 'creator'
    cid = scrapy.Field()
    banner = scrapy.Field()
    name = scrapy.Field()
    intro = scrapy.Field()
    like_counts = scrapy.Field()
    fans_counts = scrapy.Field()
    follow_counts = scrapy.Field()
    location = scrapy.Field()
    career = scrapy.Field()


class crItem(scrapy.Item):
    table_name = 'copyright'
    pcid = scrapy.Field()
    cid = scrapy.Field()
    pid = scrapy.Field()
    role = scrapy.Field()
