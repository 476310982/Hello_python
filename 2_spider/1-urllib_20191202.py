#python自带模块
import urllib.request
import gzip

#目前较为流行的模块
import requests

if __name__ == '__main__':
    # url = 'http://www.baidu.com'
    url = 'http://www.qq.com'
    response = urllib.request.urlopen(url=url)
    # print(type(response))#<class 'http.client.HTTPResponse'>
    # print(response.info())
    print(response.getcode())#200
    #print(response.read())#输出的是字节类型数据，需要转成utf-8（默认）
    #'''b'<!DOCTYPE html>\n<!--STATUS OK-->\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\....'''
    # print(response.read().decode('utf-8'))
    # print(response.read().decode('gbk'))
    b = response.read()
    #使用了gzip进行了解压缩，获得了字节数据，再进行对象得编码转化
    data = gzip.decompress(b).decode('gbk')
    print(data)
