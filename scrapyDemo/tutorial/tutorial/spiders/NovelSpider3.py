import scrapy
import os

#网站有反爬虫机制

class NovelSpider(scrapy.Spider):
    name = 'novel3'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Cookie':'ZHID=1575291837744ZHRICFWW65ULB9HSJ01; zh_visitTime=1575291837746; Hm_up_c202865d524849216eea846069349eb9=%7B%22uid_%22%3A%7B%22value%22%3A%221575291837744ZHRICFWW65ULB9HSJ01%22%2C%22scope%22%3A1%7D%7D; v_user=http%3A%2F%2Fhao123.zongheng.com%2Fbook%2F1%2F472776.html%7Chttp%3A%2F%2Fbook.zongheng.com%2Fshowchapter%2F472776.html%7C55040691; rSet=1_3_1_14; ver=2018; zhffr=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216ec6b60a4d2fa-0be161d811899b-3d644509-1327104-16ec6b60a4e7c2%22%2C%22%24device_id%22%3A%2216ec6b60a4d2fa-0be161d811899b-3d644509-1327104-16ec6b60a4e7c2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_c202865d524849216eea846069349eb9=1575291838,1575888166; JSESSIONID=abcQ0YeM8cWpf_WOvqQ7w; Hm_lpvt_c202865d524849216eea846069349eb9=1575889345; platform=H5; PassportCaptchaId=0dc8522486c5b91435367e7290c6d6ad; AST=157589890827343fe1eaefd; zhUserType=1'
    }


    def isExistsDir(self, inpath):
        find_path = "./source/" + inpath
        if not os.path.exists(find_path):
            os.makedirs(find_path)
            print(find_path, '目录创建成功')

    def start_requests(self):
        start_url = 'http://book.zongheng.com/store/c0/c0/b0/u5/p1/v0/s1/t4/u0/i1/ALL.html'
        yield scrapy.Request(url=start_url,callback=self.parse_novel_list,headers=self.headers)

    def parse_novel_list(self, response):
        novel_list = response.xpath('//div[contains(@class,"bookname")]/a/@href').getall()
        # print(novel_list)
        for url in novel_list:
            # print("url:%s" % url)
            yield response.follow(url,callback=self.parse_novel_main)
        # url = 'http://book.zongheng.com/book/874510.html'
        # yield response.follow(url,callback=self.parse_novel_main)


    def parse_novel_main(self, response):
        chapter_list = response.xpath('//div[contains(@class,"fr link-group")]/a[1]/@href').getall()
        # print(chapter_list)
        for url in chapter_list:
            print('*'*20+'\n'+url)
            yield response.follow(url,callback=self.parse_chapter)

    def parse_chapter(self,response):
        novel_list = response.xpath('//div[@class="volume-list"]/div[1]/ul/li[1]/a/@href').getall()
        for url in novel_list:
            print('*'*20+'\n'+url)
            yield response.follow(url,callback=self.parse)


    def parse(self, response):
        book_id = response.xpath('//body/@bookname').get()
        title = response.xpath('//div[@class="reader_box"]//div[@class="title_txtbox"]/text()').get().replace('\t',' ')
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
        self.isExistsDir('')
        try:

            with open('./source/%s.txt' % book_id, mode='a',encoding='utf-8') as f:
                f.write(title + '\n作者：' + author + ',字数：' + words + ',更新时间：' + last_time + '\n' + "".join(novel_content))
                f.write('\n')
            print('%s下载成功！' % (title))

            # 判断是否有下一页
            next_page = response.xpath('//div[@class="reader_box"]/div[@class="chap_btnbox"]/a[3]/@href').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                # 直接获取到下一页的绝对url，yield一个新Request对象
                # yield scrapy.Request(next_page, callback=self.parse)
                # 作用同上，不用获取到绝对的url，使用follow方法会自动帮我们实现
                yield response.follow(next_page, callback=self.parse)
        except Exception as e:
            d1 = dict({
                "小说ID": book_id,
                "章节名称：": title,
                "作者：": author,
                "字数：": words,
                "更新时间：": last_time,
                "正文：": novel_content,
            })
            print('*'*100)
            print("%s 错误章节：%s" % (book_id,title))
            print(d1)