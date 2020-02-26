import requests
import lxml
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
response = requests.get('https://maoyan.com/films/1215605',headers = headers)
print(response.status_code)
print(response.text)
