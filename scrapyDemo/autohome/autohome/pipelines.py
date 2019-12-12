# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from urllib import request

class AutohomePipeline(object):

    def process_item(self, item, spider):
        request.urlretrieve(url=item['img_url'],filename=item['img_name'])
        return item
