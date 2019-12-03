import requests
from lxml import etree
import time
import re
import json

if __name__ == '__main__':
    url = 'http://222.205.160.107/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su=1508190225'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=ADF18C1F2DAB735D536E187AE7DD30BE',
        'Host': '222.205.160.107',
        'Referer': 'http://222.205.160.107/jwglxt/xtgl/index_initMenu.html?jsdm=&_t=1575328026048',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    response = requests.get(url=url,headers=headers)
    html = response.text
    tree = etree.HTML(html) #<class 'lxml.etree._Element'>
    contains = tree.xpath('//div[@class="tab-content "]//div[contains(@class,"col-md")]')
    data = []
    fp = open('./source/info.txt',mode='a',encoding='utf-8')
    fp2 = open('./source/info.json',mode='w',encoding='utf-8')
    for info in contains:
        d =dict()
        titles = info.xpath('.//label/text()')
        contents = info.xpath('.//p/text()')
        # print(len(titles),len(contents))
        if len(titles) == 0:
            continue
        if len(contents) == 0:
            contents.append(' ')
        title = re.sub(r"['\n','\t','\r',' ']",'',str(titles[0]))
        content = re.sub(r"['\n','\t','\r',' ']",'',str(contents[0]))
        # print(title,content)
        d[title] = content
        data.append(d)
        fp.write(title+content+'\n')
    print(d)
    result = json.dumps(data,ensure_ascii=False)
    fp2.write(result)
    fp2.close()
    fp.close()
    # contentTitle = tree.xpath('//div[@class="tab-content "]//div[contains(@class,"col-md")]//label/text()')
    # contentText = tree.xpath('//div[@class="tab-content "]//div[contains(@class,"col-md")]//p[@class="form-control-static"]/text()')
    # # print(contentTab)
    # for title,text in zip(contentTitle,contentText):
    #     #将ElementUnicodeResult类转化为str类
    #     title = str(title)
    #     text = str(text)
    #     #正则替换
    #     title = re.sub(r"['\n','\t','\r',' ']",'',title)
    #     text = re.sub(r"['\n','\t','\r',' ']",'',text)
    #     print(title,text)