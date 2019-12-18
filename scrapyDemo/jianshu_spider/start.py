from scrapy import cmdline
from selenium import webdriver
#为了方便启动爬虫
if __name__ == "__main__":
    cmdline.execute("scrapy crawl jianshu".split(" "))
    # option = webdriver.ChromeOptions()
    # option.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    # browser = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe',chrome_options=option)
    # browser.get('https://www.baidu.com')