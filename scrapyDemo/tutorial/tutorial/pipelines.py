# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class NovelPipeline(object):
    def __init__(self):
        self.fp = open('./source/novel.json', mode='a', encoding='utf-8')

    def open_spider(self,spider):
        print("准备写入json文件......")

    def close_spider(self,spider):
        print("关闭文件流......")
        self.fp.close()

    def process_item(self, item, spider):
        print(item['book_id'])
        item = dict(item)
        item_json = json.dumps(item,ensure_ascii=False)
        self.fp.write(item_json + '\n')
        print("正在写入......")
