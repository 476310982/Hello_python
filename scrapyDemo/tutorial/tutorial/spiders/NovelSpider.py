import scrapy
import os

class NovelSpider(scrapy.Spider):
    name = 'novel'

    def start_requests(self):
        start_url = ['http://book.zongheng.com/chapter/882922/58099646.html','http://book.zongheng.com/showchapter/885734.html']

        for url in start_url:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def isExistsDir(self):
        if not os.path.exists('./source'):
            os.mkdir('./source')

    def parse(self,response):
        self.isExistsDir()
        title =  response.xpath('//div[@class="reader_box"]//div[@class="title_txtbox"]/text()').get()
        author = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/a[1]/text()').get()
        words = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[1]/text()').get()
        last_time = response.xpath('//div[@class="reader_box"]//div[@class="bookinfo"]/span[2]/text()').get()
        novel_content = response.xpath('//div[@class="reader_box"]//div[@class="content"]/p/text()').getall()
        with open('./source/%s.txt'%(title),mode='w',encoding='utf-8') as f:
            f.write(title[0] + '\n作者：' + author[0] + ',字数：' + words[0] + ',更新时间：' + last_time[0] + '/n' + novel_content[0])
        print('./source/%s 下载成功！'%(title))
        # yield {
        #     "章节名称：":title,
        #     "作者：":author,
        #     "字数：":words,
        #     "更新时间：":last_time,
        #     "正文：":novel_content,
        # }
        next_page = response.xpath('//div[@class="reader_box"]/div[@class="chap_btnbox"]/a[3]/@href').get()
        if not next_page is None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
        else:
            print('全部下载完成！')






