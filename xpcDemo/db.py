import time
import datetime
import pymysql
from pymysql.cursors import DictCursor


class mysqlConn(object):
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
            print('*' * 60)
            print('%s 数据库连接成功...' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            print('*' * 60)

    def process_conn(self):
        self.sql = "insert into `video` (pid,thumbnail,title,cate,created_at,play_counts,like_counts,descr,video,cover,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(self.sql,('10667943', pymysql.escape_string('https://cs.xinpianchang.com/uploadfile/article/2020/02/06/5e3be705241b8.jpeg@540w_324h_1e_1c.jpg'), '结局心碎获奖短片《慢跑》', '剧情短片-其他', '02-06 17:55', '30746', '246', '男主得到了自己心仪的警察学院录取通知，兴奋的他开始了自己早间的慢跑活动。突然发现一名男子正在追逐一个女人。正义的他报警后赶了过去...', pymysql.escape_string('https://qiniu-xpc4.xpccdn.com/5e3be2b5324bc.mp4'), pymysql.escape_string('https://cs.xinpianchang.com/uploadfile/article/2020/02/06/5e3be2a5a27c2.jpeg'), 396632))
        self.conn.commit()
        # cover = pymysql.escape_string(
        #     'https://cs.xinpianchang.com/uploadfile/article/2020/02/06/5e3be705241b8.jpeg@540w_324h_1e_1c.jpg')
        # print(cover)
        print('插入成功....')


if __name__ == '__main__':
    conn = mysqlConn()
    conn.process_conn()