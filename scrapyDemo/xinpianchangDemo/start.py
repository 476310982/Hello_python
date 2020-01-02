import re
import requests
import json
import string
import random
from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute('scrapy crawl xpc'.split(' '))
    # response = requests.request(url='https://app.xinpianchang.com/comments?resource_id=10631395',method='get')
    #
    # content = json.loads(response.text)
    # list = content['data']['list']
    # comments = []
    # for item in list:
    #     comment = {}
    #     comment['pid'] = 'pid'
    #     comment['userid'] = item['userid']
    #     comment['content'] = item['content']
    #     comment['username'] = item['userInfo']['username']

    # keys = ['1','2','3']
    # values = ['zs','ls','ww']
    # k_v = dict(zip(keys,values))
    # print(k_v)
    chars1 = [chr(i) for i in range(97, 97 + 26)]
    chars2 = [str(i) for i in range(10)]
    chars = chars1 + chars2
    # print(len(chars))
    # for i in chars:
    #     print(i)
    # print("".join(random.choices(chars, k=26)))
    # print("".join(random.choices(string.ascii_lowercase + string.digits,k=26)))
