from scrapy import cmdline
import re

if __name__ == '__main__':
    cmdline.execute('scrapy crawl sfw'.split(' '))
