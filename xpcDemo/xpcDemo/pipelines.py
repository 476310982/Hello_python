# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi


class XpcdemoPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'scrapy_db',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }

        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = ""
        if self.conn:
            print('*' * 60)
            print('数据库连接成功...')
            print('*' * 60)

    # @property
    # def sql(self):
    #     if not self._sql:
    #         self._sql = "insert into %s (%s) values (%s)"
    #         return self._sql
    #     return self._sql

    def process_item(self, item, spider):
        # flag = self.cursor.execute(self.sql,('002_002','002','002','导演'))
        keys, values = zip(*item.items())
        # print('=' * 60)
        # print(keys, values)
        values = list(map(lambda x: pymysql.escape_string(x) if isinstance(x, str) else x, values))
        self.sql = "insert into `{}` ({}) values ({})".format(item.table_name, ','.join(keys),
                                                              ','.join(['%s'] * len(values)))
        # print(values)
        # print("*" * 60)
        # print(self.sql)
        self.cursor.execute(self.sql, values)
        self.conn.commit()
        print("*" * 60)
        print('插入成功...')
        # print(flag)
