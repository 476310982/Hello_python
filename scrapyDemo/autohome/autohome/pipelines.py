# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from urllib import request
import os
from scrapy.pipelines.images import ImagesPipeline
from autohome.settings import IMAGES_STORE


class AutohomePipeline(object):
    def __init__(self):
        # os.path.dirname(__file__)：找到当前py文件的所在目录
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        # 判断文件是否存在
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']
        category_path = os.path.join(self.path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        for url in urls:
            filename = url.split('__')[-1]
            request.urlretrieve(url, os.path.join(category_path, filename))
        return item


# 重写ImagesPipeline的方法
class AutoHomeImagesPipeline(ImagesPipeline):

    # 获取请求列表的方法，使其携带item
    def get_media_requests(self, item, info):
        request_objs = super(AutoHomeImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    # 获得下载路径以及图片名称
    def file_path(self, request, response=None, info=None):
        filename = super(AutoHomeImagesPipeline, self).file_path(request, response, info).replace('full/', '')
        category = request.item.get('category')
        # category = request.item['category']
        category_path = os.path.join(IMAGES_STORE, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        img_path = os.path.join(category_path, filename)
        return img_path
