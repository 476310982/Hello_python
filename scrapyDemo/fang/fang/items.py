# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    sale = scrapy.Field()
    origin_url = scrapy.Field()
