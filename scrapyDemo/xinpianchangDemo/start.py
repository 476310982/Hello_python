import re
import requests
import json
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
