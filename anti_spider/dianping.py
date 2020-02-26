import requests
import re
import lxml
from lxml import html,etree
cookies = {
    '_lxsdk_cuid':'16cf25c6ec9c8-06f501607456d1-3d644509-144000-16cf25c6ec9c8',
	'_lxsdk':'16cf25c6ec9c8-06f501607456d1-3d644509-144000-16cf25c6ec9c8',
	'Hm_lvt_e6f449471d3527d58c46e24efb4c343e':'1567434240',
	'_hc.v':'bf0c0912-3e1f-7303-8758-c78969280798.1567434240',
	'cy':'1011',
	'cye':'huian',
	's_ViewType':'10',
	'_lx_utm':'utm_source%3Dbing%26utm_medium%3Dorganic',
	'dplet':'056ff89c6c33e0e48884df87f2ad60b1',
	'dper':'a28a7635aa007dd395f5b85d50200c9f67ea87b6a5462593779c161f77befc580374b2963ea6cf9665ae55b20a1102595c28ddfdc6b60d16e7007bc522ad258785858ce8557b84d056cb29161bf9fd309d4cbace34427202f8e4c1e9ec8640d2',
	'll':'7fd06e815b796be3df069dec7836c3df',
	'ua':'dpuser_6434765948',
	'ctu':'71adab3e525a8bbb1ccbfba26a620a97e64be00e04b68618b1443cea595c5d0b',
	'_lxsdk_s':'1707125b59b-4f8-8dd-7a5%7C%7C258'
}

if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    response = requests.get('http://www.dianping.com/huian/ch10',headers = headers,cookies = cookies)
    print(response.status_code)
    # selector = etree.HTML(response.text)
