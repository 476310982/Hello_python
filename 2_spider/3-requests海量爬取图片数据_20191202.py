import requests
import re

if __name__ == '__main__':
    # http://sc.chinaz.com/tupian/meinvxiezhen_2.html
    url = 'http://sc.chinaz.com/tupian/meinvxiezhen_2.html'
    response = requests.get(url=url)
    html = response.text

    #正则表达式
    # "?"表示非贪婪匹配模式，遇到第一个结果立刻返回
    pattern = r'<img src2="(.*?)" .*?>'

    image_urls = re.findall(pattern,html)
    print(image_urls, len(image_urls),sep='\n')
