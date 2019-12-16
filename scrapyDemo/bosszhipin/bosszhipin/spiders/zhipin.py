# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bosszhipin.items import BosszhipinItem

class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1']
    # start_urls = ['https://www.zhipin.com/job_detail/8442917f2a0c84b21XFy2Nm_ElU~.html']
    # 'https://www.zhipin.com/job_detail/8442917f2a0c84b21XFy2Nm_ElU~.html'
    rules = (
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'.+job_detail/.+.html'), callback="parse", follow=False),
    )

    def parse(self, response):
        print('='*60)
        name = response.xpath('//div[@class="info-primary"]/div/h1/text()').extract_first()[0]
        salary = response.xpath('//div[@class="info-primary"]/div/span/text()').extract()[0]
        infos = response.xpath('//div[contains(@class,"job-primary")]/div[@class="info-primary"]/p/text()').extract()
        city = infos[0]
        work_years = infos[1]
        education = infos[2]
        company = response.xpath(
            '//div[@class="sider-company"]//div[@class="company-info"]/a[1]/@title').extract()[0]
        item = BosszhipinItem(name=name, salary=salary, city=city, work_years=work_years, education=education,
                        company=company)
        print(name,salary,infos)
        yield item
        # return item
