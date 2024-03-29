from scrapy import cmdline
from urllib import request
from base64 import b64encode
import tesserocr
import requests
from PIL import Image

# def recognize_valid(img):
#     image = Image.open(img)
#     # image.show()
#     print(tesserocr.image_to_text(image))
#     print(tesserocr.get_languages())

def recognize_valid(img_url):
    api_url = 'https://imgurlocr.market.alicloudapi.com/urlimages'
    appcode = 'f6ada03339e0421881791126c4dea4fd'
    request.urlretrieve(url=img_url, filename='dyejValid.png')
    body = {}
    with open('dyejValid.png', mode='rb') as fp:
        img_data = fp.read()
        pic = b64encode(img_data)
        pic = 'data:image/jpeg;base64,' + str(pic, encoding='utf-8')
        body['image'] = pic
    headers = {
        'Authorization': 'APPCODE ' + appcode,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
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


if __name__ == '__main__':
    # img_url = 'https://fj.dyejia.cn/partysso/index/validImg?tm=1576115873828'
    # # img = 'validImg.png'
    # recognize_valid(img_url)

    cmdline.execute('scrapy crawl dyej_spider'.split(' '))
