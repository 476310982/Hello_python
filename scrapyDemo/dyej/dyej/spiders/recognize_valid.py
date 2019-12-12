from urllib import request
from base64 import b64encode
import requests


def recognize_valid(img_url):
    #图像识别Api接口属性
    api_url = 'https://imgurlocr.market.alicloudapi.com/urlimages'
    appcode = 'f6ada03339e0421881791126c4dea4fd'
    headers = {
        'Authorization': 'APPCODE ' + appcode,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    #post请求体
    body = {}
    #请求验证码链接，下载并保存
    request.urlretrieve(url=img_url, filename='dyejValid.png')
    #读取验证码字节数据,并进行base64b编码,转为str,传入请求体
    with open('dyejValid.png', mode='rb') as fp:
        img_data = fp.read()
        pic = b64encode(img_data)
        pic = 'data:image/jpeg;base64,' + str(pic, encoding='utf-8')
        body['image'] = pic

    #接口返回api识别结果（json数据）
    response = requests.post(api_url, data=body, headers=headers)
    if response.status_code == 200:
        res = response.json()
        print(res)
        if res['result_num'] != 0:
            validcode = res['result'][0]['words'].replace(' ','').strip()
            print(validcode)
            return validcode
    else:
        return None