# coding:utf-8
import requests
import re
import time

if __name__ == '__main__':
    try:
        COUNT = 0
        # 定义正则表达式
        pattern = '<a  href="(.*?)" .*>(.*?)</a>'
        # pattern2 = '<p>(.*)</p>'
        pattern2 = '<div class="content".*?<p>(.*)</p>\r'
        # 小说目录url
        url = 'http://book.zongheng.com/showchapter/472776.html'
        # 获得目录内容
        html = requests.get(url).text
        # 根据正则表达式获得目录url以及小说章节标题
        txt = re.findall(pattern, html)
        txt_urls = [index[0] for index in txt]
        txt_names = [index[1] for index in txt]
        # 循环爬取每章小说
        for txt_url, txt_name in zip(txt_urls, txt_names):
            if txt_name == '':
                continue
            content = re.findall(pattern2, requests.get(txt_url).text, re.S)
            # 清洗
            txt_content = content[0].replace('</p><p>', '\n')
            # 写入文件
            with open('./Datas/%s.txt' % (txt_name), mode='w', encoding='utf-8') as fp:
                fp.write(txt_content)
            print('%s\t下载完成!' % (txt_name))
            time.sleep(1)
            COUNT += 1
            if COUNT == 10:
                break
    except Exception as e:
        print('爬取小说异常')
    finally:
        print('下载完成')
