import requests
import re
import time

if __name__ == '__main__':
    try:
        COUNT = 0
        pattern = r'<img src2="(.*?)" .*?>'
        url1 = 'http://sc.chinaz.com/tupian/xingganmeinvtupian.html'
        url2 = 'http://sc.chinaz.com/tupian/xingganmeinvtupian_%d.html'
        for i in range(3):
            if i == 0:
                url = url1
            else:
                url = url2 % (i + 1)
            html = requests.get(url).text
            # print(html)
            # print(response.text)
            img_urls = re.findall(pattern, html)
            img_names = [img.split('/')[-1] for img in img_urls]
            # print(img_name)
            # print(img_urls)
            for img_url, img_name in zip(img_urls, img_names):
                img = requests.get(img_url).content
                with open('./Pictures/Beauties/%s' % (img_name), mode='wb') as fp:
                    fp.write(img)
                time.sleep(2)#防止网站检测出爬虫
                print('第%d页图片%s下载完成！' % (i + 1, img_name))
                COUNT += 1
            print('*' * 100)
    except Exception as e:
        with open('./爬虫异常log.txt', mode='a', encoding='utf-8') as fp:
            fp.write(e, '\n')
        print('程序异常结束，请查看日志')
    finally:
        print('累计爬取了%d张图片'%COUNT)