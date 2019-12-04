import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://search.51job.com/list/110200,000000,0000,00,9,99,%s,2,1.html'
    key = input("请输入您想查询的职业:")
    response = requests.get(url=url%(key))
    # print(response.status_code)
    response.encoding = 'gbk'
    html = response.text
    tree = etree.HTML(html)
    # print(type(tree))#<class 'lxml.etree._Element'>
    divs = tree.xpath('//div[@class="dw_table"]//div[@class="el"]')
    for div in divs:
        try:
            # print(etree.tostring(div,encoding='utf-8').decode('utf-8'))
            job = div.xpath('.//p[contains(@class,"t1")]//a/@title')[0]
            com = div.xpath('.//span[@class="t2"]/a/text()')[0]
            add = div.xpath('.//span[@class="t3"]/text()')[0]
            date = div.xpath('.//span[@class="t5"]/text()')[0]
            sal = div.xpath('.//span[@class="t4"]/text()')[0]  # 该字段可能出现空
        except Exception as e:
            sal = '面议'
        finally:
            with open('./source/51job_Info.txt', mode='a', encoding='utf-8') as fp:
                fp.write('职位：%s 公司：%s 地点：%s 薪资：%s 发布时间：%s\n' % (job, com, add, sal, date))
    print('爬取完成')
            # print(job, com, add, sal, date, sep='   ')
