from scrapy import cmdline
#为了方便启动爬虫
if __name__ == "__main__":
    cmdline.execute("scrapy crawl jianshu".split(" "))