from scrapy import cmdline
import re

if __name__ == '__main__':
    cmdline.execute('scrapy crawl sfw'.split(' '))
    # pattern = r'\d+(?:~\d+)?平米'
    # str = ' 140~172平米 '
    # res = re.findall(pattern, str)
    # print (res)
