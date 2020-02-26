import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyexcel

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.qunar.com/')
    # 在等待页面加载完成并判断指定事件
    dest = WebDriverWait(driver,10,ignored_exceptions=True).until(
        # EC.presence_of_all_elements_located((By.XPATH,'//div[@class="qunar-qcbox"]/input[@name="toCity"]'))
        EC.element_to_be_clickable((By.XPATH,'//div[@class="qunar-qcbox"]/input[@name="toCity"]'))
    )
    dest = driver.find_element_by_xpath('//div[@class="qunar-qcbox"]/input[@name="toCity"]')
    dest.send_keys('上海')
    dest.click()
    # 隐式等待1秒
    driver.implicitly_wait(1)
    print('已经点击')
    time.sleep(1)
    dest.send_keys(Keys.RETURN)
    # search_brn = driver.find_element_by_css_selector('button.button-search')
    # search_brn.click()
