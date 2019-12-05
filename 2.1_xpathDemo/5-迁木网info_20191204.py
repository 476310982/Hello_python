import requests
import os
from lxml import etree

if __name__ == '__main__':
    url = 'http://www.qianmu.org/ranking/1528.htm'
    headers = {
        'Cookie': 'JSESSIONID=F144F6AE06CB289121270968F8EEC6FE; Hm_lvt_f409979f9c1034edcba2b24ea2b0a835=1575461155,1575469125; MEIQIA_VISIT_ID=1UWJvkpHE10XDko0MU7WR9IijeE; Hm_lpvt_f409979f9c1034edcba2b24ea2b0a835=1575469336',
        'Host': 'www.qianmu.org',
        'Referer': 'http://www.qianmu.org/ranking/1528.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    headers2 = {
        'Cookie': 'JSESSIONID=0CA86929BECB86935BF0B816A3FD0C3A; Hm_lvt_f409979f9c1034edcba2b24ea2b0a835=1575461155; MEIQIA_VISIT_ID=1UWJvkpHE10XDko0MU7WR9IijeE; Hm_lpvt_f409979f9c1034edcba2b24ea2b0a835=1575468220',
        'Host': 'www.qianmu.org',
        'Referer': 'http://www.qianmu.org/nextfill',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    response = requests.get(url=url,headers=headers)
    # print(response.text)
    fatherHtml = response.text
    tree = etree.HTML(fatherHtml)
    # print(type(tree))
    nodes = tree.xpath('//table//a[1]/@href')
    # print(len(nodes))#731
    for node in nodes[0:1]:
        response = requests.get(url=node,headers=headers2)
        print(response.text)