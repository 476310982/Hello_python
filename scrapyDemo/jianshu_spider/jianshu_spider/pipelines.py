# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi


# 对接收到的item进行处理 可进行数据持久化（存入数据库） 也可以写入到json文件或者其他格式的文件内


class JianshuSpiderPipeline(object):
    # 初始化mysql数据库连接
    # 使用一个数据库连接则为同步插入数据

    def __init__(self):
        # 数据库连接参数
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,  # 端口号是int类型
            'user': 'root',
            'password': 'root',
            'database': 'scrapy_db',
            'charset': 'utf8'  # 有必要声明字符集，数据库字符集不带“-”
        }
        # **dbparams 代表解开dbparams字典，将其键值对作为参数传入
        self.conn = pymysql.connect(**dbparams)
        # 用cursor游标来执行数据操作
        self.cursor = self.conn.cursor()
        self._sql = ""
        # 判断数据库是否连接成功
        if self.conn:
            print('=' * 60)
            print('数据库连接成功....\n{}'.format(self.conn))
            print('=' * 60)

    # 使用python装饰器，将方法装饰成属性，可以直接调用
    @property
    def sql(self):
        if not self._sql:
            # 声明sql语句
            self._sql = 'insert into article(id,title,author,content,origin_url,article_id,read_count,word_count,subjects) values (null,%s,%s,%s,%s,%s,%s,%s,%s)'
            return self._sql
        return self._sql

    # 对接收到的item进行处理
    def process_item(self, item, spider):
        print('插入文章标题：{},网址：{}'.format(item['title'], item['origin_url']))
        # 用数据库游标执行sql语句，并传入参数元组（args1，args2...）
        self.cursor.execute(self.sql,
                            (item['title'], item['author'], item['content'], item['origin_url'], item['article_id'],
                             item['read_count'], item['word_count'], item['subjects']))
        # 提交数据
        self.conn.commit()
        return item


# 数据库连接池 异步插入数据 理论上插入速度比同步的快 运用了scrapy框架底层提供的Twisted-defer方法
class JianshuTwistedSpiderPipeline(object):
    # 一分钟半68条
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'scrapy_db',
            'charset': 'utf8',
            'cursorclass': DictCursor  # 定义游标类型
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = 'insert into article(id,title,author,content,origin_url,article_id) values (null,%s,%s,%s,%s,%s)'
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # 与数据库交互并返回结果，传入方法、参数
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 添加异常回调函数
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql,
                       (item['title'], item['author'], item['content'], item['origin_url'], item['article_id']))

    # 定义异常回调函数，打印error，不影响其他操作
    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(error)
        print('=' * 10 + 'error' + '=' * 10)
