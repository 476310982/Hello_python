from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute("scrapy crawl httpbin".split(' '))
    cmdline.execute("scrapy crawl httpbin_ip".split(' '))