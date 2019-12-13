# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#定义数据格式
class AutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()

    #imagepipeline 必须有的2个属性
    image_urls = scrapy.Field()
    images = scrapy.Field()
