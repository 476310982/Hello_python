import requests
import os

if __name__ == '__main__':
    # response = requests.get('http://book.zongheng.com/chapter/764228/42488060.html')
    # print(response.content)
    # bookId = '7888888'
    if not os.path.exists('./source'):
        os.makedirs('./source')
    # curr_dir = os.getcwd()
    # print(curr_dir)
    #
    # last_dir = os.path.join(curr_dir,bookId)
    # print(last_dir)
    # with open('./source/%s/%s.txt'%(bookId,"张三"),mode='w') as f:
    #     f.write('Hello Python')
