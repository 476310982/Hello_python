# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoInfoItem(scrapy.Item):
    # define the fields for your item here like:
    pid = scrapy.Field()
    title = scrapy.Field()
    video_url = scrapy.Field()
    category = scrapy.Field()
    update_time = scrapy.Field()
    curplaycounts = scrapy.Field()
    like_counts = scrapy.Field()
    desc = scrapy.Field()
    tags = scrapy.Field()
    duration = scrapy.Field()
    video_cover = scrapy.Field()
    creator_info = scrapy.Field()


class CommentsItem(scrapy.Item):
    pid = scrapy.Field()
    userid = scrapy.Field()
    content = scrapy.Field()
    username = scrapy.Field()
