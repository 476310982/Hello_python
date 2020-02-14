from scrapy import cmdline
from fake_useragent import UserAgent
import re
import string
import random
import pymysql
from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi


def delComma(str):
    return "".join(str.split(","))


if __name__ == '__main__':
    # conn = mysqlconn()
    # conn.process_option()
    cmdline.execute("scrapy crawl xpc".split(" "))

# print(string.digits)
# print(string.ascii_lowercase)
# print(string.ascii_letters)
# print(string.ascii_uppercase)
# print(string.capwords("happy"))
# print(string.hexdigits)
# print(string.octdigits)
# lst = string.digits + string.ascii_lowercase
# print(lst)
# sessionId = random.choices(lst,k=26)
# print(''.join(sessionId))

#
# s1 ="7321"
# print(delComma(s1))
# res = "".join(s1.split(","))
# print(res)
# ua=UserAgent()
# print(ua.random)
