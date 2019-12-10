# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    words = scrapy.Field()
    last_time = scrapy.Field()
    novel_content = scrapy.Field()
