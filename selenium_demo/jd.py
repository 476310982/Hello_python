import sys
import time
import pyexcel

from selenium import webdriver
# keys包含特殊的键位，例如回车[RETURN]
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from mysqldb import mysqlPipeline

if __name__ == '__main__':
    db = mysqlPipeline()
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    driver.get('https://www.jd.com/')
    # 获取首页输入框的控制，输入关键词并按回车操作
    kw = driver.find_element_by_id('key')
    kw.send_keys(keyword)
    kw.send_keys(Keys.RETURN)
    # 跳转到搜索结果页面
    print(driver.current_url)
    time.sleep(3)
    print('跳转成功')
    # 实现点击排序按钮：按照销量排序展示结果
    sort_btn = driver.find_element_by_xpath('//div[@class="f-sort"]/a[2]')
    sort_btn.click()
    has_next = True
    while has_next:
        time.sleep(3)
        # 获取列表尺寸
        good_list = driver.find_element_by_id('J_goodsList').rect
        height = good_list['y'] + good_list['height']
        for i in range(10):
            driver.execute_script('window.scrollTo(0,%s)' % (i * 1000))
            time.sleep(3)
            if i > height:
                break
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        lis = driver.find_elements_by_class_name('gl-item')
        time.sleep(2)
        print('获取成功')
        rows = []
        for li in lis:
            info = {}
            info['sku'] = sku = li.get_attribute('data-sku')
            info['price'] = li.find_element_by_class_name('p-price').text
            info['name'] = li.find_element_by_css_selector('div.p-name>a>em').text
            info['comments'] = li.find_element_by_id('J_comment_%s' % sku).text
            info['shop'] = li.find_element_by_css_selector('div.p-shop>span>a').text
            info['goods_url'] = li.find_element_by_css_selector('div.p-img>a').get_attribute('href')
            info['img_url'] = li.find_element_by_css_selector('div.p-img>a>img').get_attribute('src')
            # 将数据存入mysql数据库
            db.process_item(info)
            # 将数据存入列表，最后生成excel表格
            rows.append(info)
        try:
            curPage = driver.find_element_by_css_selector('span.p-num>a.curr').text
            print('=' * 20 + '已获取第%s页内容,共有%s件商品' % (curPage, len(lis)) + '=' * 20)
            driver.save_screenshot('第%s页面截图.png' % curPage)
            next_page = driver.find_element_by_class_name('pn-next')
            if 'disabled' in next_page.get_attribute('class'):
                has_next = False
            else:
                next_page.click()
        except:
            has_next = False
    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)
    driver.quit()
