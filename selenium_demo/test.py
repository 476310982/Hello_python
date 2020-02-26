
import pyexcel
import selenium
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com')
    # print(driver.page_source)
    driver.execute_async_script()