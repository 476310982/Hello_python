# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# 中间件 通常用来定义随机UA标识，设置IP代理池
import time

from scrapy import signals
# pip install selenium
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse


# class JianshuSpiderSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
#
# class JianshuSpiderDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)

# 自定义下载中间件
class JianshuSeleniumDownloadMiddleware(object):
    # 创建web驱动，声明执行的控件绝对路径
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=option)

    # 定义爬虫下载前操作
    def process_request(self, request, spider):
        # 接收engine（引擎）发送过来的请求url，驱动发送GET请求
        self.driver.get(request.url)
        # 为了等待驱动获取页面完整，等待一秒
        time.sleep(1)
        try:
            # 渲染的页面中存在需要多次点击【展开更多】的可能，故设置循环
            while True:
                # 获取节点对象
                showMore = self.driver.find_element_by_class_name('H7E3vT')
                # 点击节点对象
                showMore.click()
                time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        # 获取网页源代码
        source = self.driver.page_source
        # 返回信息，将当前url、页面源代码、请求对象以及字符编码返回
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        # 不会经过scrapy的download组件
        return response
