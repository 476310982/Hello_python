# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#对接收到的item进行处理 可进行数据持久化（存入数据库） 也可以写入到json文件或者其他格式的文件内
class JianshuSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
