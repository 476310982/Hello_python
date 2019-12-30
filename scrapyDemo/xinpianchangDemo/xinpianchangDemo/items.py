# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XinpianchangdemoItem(scrapy.Item):
    # define the fields for your item here like:
    video_name = scrapy.Field()
    video_url = scrapy.Field()
    cates = scrapy.Field()
    update_time = scrapy.Field()
    curplaycounts = scrapy.Field()
    like_counts = scrapy.Field()
    desc = scrapy.Field()
    info_tags = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
    # name = scrapy.Field()
