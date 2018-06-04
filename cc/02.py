import time
from lxml import etree
from selenium import webdriver


browser = webdriver.Chrome(executable_path=r"C:\Projects\virtualenv\python_03env\Scripts\chromedriver.exe")

# http://www.aeonweb.cn/AeonACH/SignIn.aspx
# 0000203145
# 111111

def get_page():
    base_url = 'http://www.aeonweb.cn/AeonACH/SignIn.aspx'
    browser.get(base_url)
    time.sleep(1)
    browser.find_element_by_id('TxtUser').send_keys('0000203145')
    time.sleep(1)
    browser.find_element_by_id('TxtPassword').send_keys('111111')
    time.sleep(1)
    browser.find_element_by_id('btnLogin').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnAgree').click()
    time.sleep(1)
    browser.find_element_by_id('btnTransCheckSys').click()
    time.sleep(1)
    browser.find_element_by_id('btnInput').click()
    time.sleep(1)

    for count in range(44):
        count += 1
        browser.find_element_by_id('ShopList1_ddlShopList').click()
        time.sleep(1)
        rule = '//select/option[%d]' %count
        browser.find_element_by_xpath(rule).click()
        time.sleep(4) # 因为需要加载页面,所以需要等候时间长一点儿
        html = browser.page_source
        html = etree.HTML(html)
        remind = html.xpath('//span[@id="Lab_MSG"]/text()')[0]
        print(remind)
        if '对不起' in remind:
            continue  # 终止本次循环 , 进行下一次循环
        elif '被[AEON]财务确认' in remind:
            continue
        else:
            # 点击确认
            browser.find_element_by_id('btnInput').click()
            time.sleep(1)
            # 返回
            browser.find_element_by_id('btnBack').click()
            time.sleep(1)


if __name__ == '__main__':
    get_page()
