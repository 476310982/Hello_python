import scrapy
import os
import re


class NovelSpider(scrapy.Spider):
    name = 'novel3'

    def isExistsDir(self, inpath):
        find_path = "./source/" + inpath
        print(find_path)
        if not os.path.exists(find_path):
            os.makedirs(find_path)
            print(find_path, '目录创建成功')

    def start_requests(self):
        start_url = 'http://book.zongheng.com/store/c0/c0/b0/u5/p1/v0/s1/t4/u0/i1/ALL.html'
        yield scrapy.Request(url=start_url,callback=self.parse_novel_list)

    def parse_novel_list(self, response):
        novel_list = response.xpath('//div[contains(@class,"bookname")]/a/@href').getall()
        # print(novel_list)
        # for url in novel_list:
        #     # print("url:%s" % url)
        #     yield response.follow(url,callback=self.parse_novel_main)
        url = 'http://book.zongheng.com/book/764228.html'
        yield response.follow(url,callback=self.parse_novel_main)


    def parse_novel_main(self, response):
        chapter_list = response.xpath('//div[contains(@class,"fr link-group")]/a[1]/@href').getall()
        # print(chapter_list)
        for url in chapter_list:
            # print('*'*20+'\n'+url)
            yield response.follow(url,callback=self.parse_chapter)

    def parse_chapter(self,response):
        novel_list = response.xpath('//div[@class="volume-list"]/div[1]/ul/li[1]/a/@href').getall()
        for url in novel_list:
            # print('*'*20+'\n'+url)
            yield response.follow(url,callback=self.parse)


    def parse(self, response):
        book_id = response.xpath('//body/@bookname').get()
        title = response.xpath('//div[@class="reader_box"]//div[@class="title_txtbox"]/text()').get()
        author = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/a[1]/text()').get()
        words = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[1]/text()').get()
        last_time = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[2]/text()').get()
        novel_content = response.xpath('//div[@class="reader_box"]//div[@class="content"]/p/text()').getall()

        # yield {
        #     "小说ID":book_id,
        #     "章节名称：":title,
        #     "作者：":author,
        #     "字数：":words,
        #     "更新时间：":last_time,
        #     "正文：":novel_content,
        # }
    #
    #
        self.isExistsDir(book_id)
        with open('./source/%s/%s.txt' % (book_id, title), mode='w') as f:
            f.write(title + '\n作者：' + author + ',字数：' + words + ',更新时间：' + last_time + '\n' + "".join(novel_content))
        print('%s下载成功！' % (title))

        # 判断是否有下一页
        next_page = response.xpath('//div[@class="reader_box"]/div[@class="chap_btnbox"]/a[3]/@href').get()
        if not next_page is None:
            next_page = response.urljoin(next_page)
            # 直接获取到下一页的绝对url，yield一个新Request对象
            # yield scrapy.Request(next_page, callback=self.parse)
            # 作用同上，不用获取到绝对的url，使用follow方法会自动帮我们实现
            yield response.follow(next_page, callback=self.parse)
