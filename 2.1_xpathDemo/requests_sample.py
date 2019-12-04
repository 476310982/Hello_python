import requests
#使用requests.Session对象请求
# 创建一个Session对象
s = requests.Session()
# session对象会保存服务器返回的set-cookies头信息里面的内容
s_head = s.get('http://httpbin.org/cookies/set/userid/123456789')
print(s_head)
# s.get('http://httpbin.org/cookies/set/token/xxxxxxxxxxxxxxxxxx')
# 下一次请求会将本地所有的cookies信息自动添加到请求头信息里面
r = s.get('http://httpbin.org/cookies')
print('检查session中的cookies', r.json())


print('不使用代理：', requests.get('http://httpbin.org/ip').json())
print('使用代理：', requests.get(
    'http://httpbin.org/ip',
    proxies={'http': 'http://iguye.com:41801'}
).json())

r = requests.get('http://httpbin.org/delay/4', timeout=3)
print(r.text)