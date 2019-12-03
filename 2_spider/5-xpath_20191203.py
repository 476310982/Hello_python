from lxml import etree
import requests
import re

if __name__ == '__main__':
    data = '''<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
    # tree = etree.HTML(data)
    # print(tree, type(tree), etree.tostring(tree).decode('utf-8'), sep='\n')

    # result = tree.xpath('//li')
    # print(result)
    # for i in result:
    #     print('*'*10,etree.tostring(i).decode('utf-8'))

    #查找特定属性的节点：[@xxx]
    # res = tree.xpath('//li[@class="item-0"]')
    # for i in res:
    #     print(etree.tostring(i).decode('utf-8'))

    #同上
    # res = tree.xpath('//li[contains(@class,"0")]')
    # for i in res:
    #     print(etree.tostring(i).decode('utf-8'))

    #按网页结构层级查找：html->body->div->ul->li
    # res = tree.xpath('/html/body/div/ul//li')
    # for i in res:
    #     print(etree.tostring(i).decode('utf-8'))

    #获取标签内容
    # res = tree.xpath('//a/text()')
    # for i in res:
    #     print(i)


    # tree = etree.parse('./Datas/test_html.html')
    # print(etree.tostring(tree,encoding='utf-8').decode('utf-8'))

    # print(tree.xpath('//li[@id="hehe"]/text()'))
    #
    # result = tree.xpath('//div[@id="pp"]//li/text()')
    # print(result)
    # for r in result:
    #     print(r)
