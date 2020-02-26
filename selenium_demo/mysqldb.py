import time
import pymysql
from pymysql.cursors import DictCursor


class mysqlPipeline(object):
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
        if self.conn:
            print('=' * 20 + '数据库连接成功' + '=' * 20)

    def process_item(self, item):
        # print(type(item))
        keys, values = item.keys(), item.values()
        values = list(map(lambda x: pymysql.escape_string(x) if isinstance(x, str) else x, values))
        # print(keys)
        # print('=' * 60)
        # print(values)
        self.sql = 'insert into `jd_goodlist`({}) values ({}) ON DUPLICATE KEY UPDATE {}'.format(
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['{}=%s'.format(k) for k in keys])
        )
        # print(self.sql)
        self.cursor.execute(self.sql, values * 2)
        self.conn.commit()
        print('=' * 20 + '插入成功' + '=' * 20)
