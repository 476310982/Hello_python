# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


# 对接收到的item进行处理 可进行数据持久化（存入数据库） 也可以写入到json文件或者其他格式的文件内
class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'scrapy_db',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = ""
        if self.conn:
            print('=' * 60)
            print('数据库连接成功....')
            print(self.conn)

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into article(id,title,author,content,origin_url,article_id) values (null,%s,%s,%s,%s,%s);
            '''
            return self._sql
        return self._sql

    def process_acticle(self, item, spider):
        print('*'*60)
        self.cursor.execute(self.sql,
                            (item['title'], item['author'], item['content'], item['origin_url'], item['acticle_id']))
        self.conn.commit()
        return item
