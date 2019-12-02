import requests
import time

if __name__ == '__main__':
    # get请求
    # url = 'http://httpbin.org/'
    # response = requests.get(url)
    # print(response.text)
    # print(response.encoding)
    # print(response.headers)

    # post请求
    # url = 'http://httpbin.org/post'
    # response = requests.post(url=url,data={'Cookie':'zhanghangyi'})
    # encoding = response.encoding
    # print(response.text)
    # print(response.content)

    # 获取图片
    # url = 'https://inews.gtimg.com/newsapp_bt/0/10834405841/1000'
    # response = requests.get(url)
    # with open('./Datas/car.jpg',mode = 'wb') as fp:
    #     content = response.content
    #     fp.write(content)
    #     print('图片保存成功！')

    # 百度贴吧
    url = 'http://tieba.baidu.com/f?kw=%E6%B3%89%E5%B7%9E%E5%9F%8E%E4%B8%9C%E4%B8%AD%E5%AD%A6&ie=utf-8&pn={}'
    for i in range(2):
        html = requests.get(url=url.format(i * 50)).text
        with open('./Datas/泉州城东贴吧第%d页.html' % (i + 1), mode='w', encoding='utf-8') as fp:
            fp.write(html)
        print('保存泉州城东贴吧第%d页成功！' % (i + 1))
        time.sleep(2)#防止百度贴吧检测出该程序为爬虫程序