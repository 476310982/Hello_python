#coding:utf-8
import requests
import re

if __name__ == '__main__':
    # url = 'http://sc.chinaz.com/tupian/meinvxiezhen_{}.html'
    # index = url.rsplit('/',maxsplit=1)
    # print(type(index))
    # print(index)
    url = 'http://book.zongheng.com/chapter/472776/7843495.html'
    pattern2 = '<div class="content".*?<p>(.*)</p>\r'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    # html ='''<div class="content" itemprop="acticleBody">
    #                    <p>五天后。</p><p>车间里，夏雷埋头干活。手控车床旁边的一只箱子里放着好几件已经加工好的精密加工件，再有一会儿时间他便算大功告成了，因为他手里的已经是最后一件精密加工件了。完成了，一百万的工钱也就算到手了。</p><p>“拿到这一百万，雷马工作室就有资金升级了。买设备，请熟练工。我没必要留在雷马工作室干那些利润很低的活，以我现在的技术，我应该成为雷马工作室的招牌，只接有难度的，或者别人干不了的活。这样的话，不仅能赚更多的钱，我也有时间干点别的事情。”一边干活，夏雷的心里一边计划着往后的事情。</p><p>这一百万给了他一个启发，以他的能力，他确实没有必要再干那些技术粗糙利润又低的活。以他的能力，要他出手，那就得像这次一样，要付得起钱才行！</p><p>'''
    # print(html)
    res = re.findall(pattern2,html,re.S)
    print(res)
