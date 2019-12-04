import requests
from lxml import etree

if __name__ == "__main__":
    url = 'http://www.xiachufang.com/'
    response = requests.get(url)
    # print(response.text)
    tree = etree.HTML(response.text)
    imgs = tree.xpath('//img[contains(@src,"http")]/@src')
    # print(imgs)
    index = 0
    for img in imgs:
        # img_url = etree.tostring(img).decode('utf-8')
        imgb = requests.get(img).content
        # print(imgb)
        with open('./source/下厨房美食图片%d.jpeg'%(index),mode='wb') as fp:
            fp.write(imgb)
        print('下厨房美食图片%d.jpeg下载完成！'%(index))
        index += 1
