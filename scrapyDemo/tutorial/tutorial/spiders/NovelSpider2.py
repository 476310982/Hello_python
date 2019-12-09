import scrapy
import os
import re


class NovelSpider(scrapy.Spider):
    name = 'novel2'

    #定义初始url，迭代返回requests并知识回调函数parse
    def start_requests(self):
        start_url = ['http://book.zongheng.com/chapter/882922/58099646.html',
                     'http://book.zongheng.com/chapter/885734/58173725.html']
        for url in start_url:
            path = re.split('/', url)[-1]
            inpath = re.split('\.', path)[0]
            # self.isExistsDir(inpath)
            yield scrapy.Request(url=url, callback=self.parse)

    #判断目录是否存在
    def isExistsDir(self, inpath):
        find_path = "./source/" + inpath
        print(find_path)
        if not os.path.exists(find_path):
            os.makedirs(find_path)
            print(find_path, '目录创建成功')

    #页面解析过程
    def parse(self, response):
        book_id = response.xpath('//body/@bookid').get()
        title = response.xpath('//div[@class="reader_box"]//div[@class="title_txtbox"]/text()').get()
        author = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/a[1]/text()').get()
        words = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[1]/text()').get()
        last_time = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[2]/text()').get()
        novel_content = response.xpath('//div[@class="reader_box"]//div[@class="content"]/p/text()').getall()
        title = title.replace(' ', '')
        self.isExistsDir(book_id)
        with open('./source/%s/%s.txt' % (book_id, title), mode='w') as f:
            f.write(title + '\n作者：' + author + ',字数：' + words + ',更新时间：' + last_time + '\n' + "".join(novel_content))
        print('%s下载成功！' % (title))

        #判断是否有下一页
        next_page = response.xpath('//div[@class="reader_box"]/div[@class="chap_btnbox"]/a[3]/@href').get()
        if not next_page is None:
            next_page = response.urljoin(next_page)
            #直接获取到下一页的绝对url，yield一个新Request对象
            # yield scrapy.Request(next_page, callback=self.parse)
            #作用同上，不用获取到绝对的url，使用follow方法会自动帮我们实现
            yield response.follow(next_page,callback=self.parse)

        # yield {

        #     "章节名称：":title,
        #     "作者：":author,
        #     "字数：":words,
        #     "更新时间：":last_time,
        #     "正文：":novel_content,
        # }
