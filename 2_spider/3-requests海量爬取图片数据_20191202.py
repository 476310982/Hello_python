import requests
import re

if __name__ == '__main__':
    # http://sc.chinaz.com/tupian/meinvxiezhen_2.html
    url = 'http://sc.chinaz.com/tupian/meinvxiezhen_{}.html'

    #正则表达式
    # "?"表示非贪婪匹配模式，遇到第一个结果立刻返回
    pattern = r'<img src2="(.*?)" .*?>'
    #翻页下载每页的图片
    for i in range(2,4):
        response = requests.get(url=url.format(i))
        html = response.text
        #正则表达匹配
        image_urls = re.findall(pattern,html)
        # print(image_urls, len(image_urls),sep='\n')
        for img_url in image_urls:
            response = requests.get(img_url)
            content = response.content
            # file = img_url.rsplit('/')[1]
            file = img_url.split('/')[-1]
            # print(file)
            with open('./Pictures/Beauties/%s'%(file),mode='wb') as fp:
                fp.write(content)
            print('成功保存图片%s'%(file))
