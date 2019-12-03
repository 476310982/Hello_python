import requests
from lxml import etree

if __name__ == '__main__':
    url1 = 'http://sc.chinaz.com/tupian/index.html'
    url2 = 'http://sc.chinaz.com/tupian/index_{}.html'
    for i in range(1,5):
        if i == 1:
            url = url1
        else:
            url =url2.format(i)
        html = requests.get(url).text
        tree = etree.HTML(html)
        img_urls = tree.xpath('//img/@src2')
        for img_url in img_urls:
            # print(img_url)
            img_name = img_url.split('/')[-1]
            # print(img_name)
            img = requests.get(img_url).content
            with open('./source/%s'%(img_name),mode='wb') as fp:
                fp.write(img)
            print('第%d页图片%s\t下载成功！'%(i,img_name))


