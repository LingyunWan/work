import time
from lxml import etree
from selenium import webdriver

import IpProxyPool
from MySql import MySql

# PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

"""
from selenium import webdriver
 
PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
 
chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("http://whatismyipaddress.com")
"""

# # 加载代理池
# proxies = IpProxyPool.get_proxy()
# print(proxies)
# # browser = webdriver.PhantomJS()
browser = webdriver.Chrome(executable_path=r"C:\Projects\virtualenv\python_03env\Scripts\chromedriver.exe")
# browser = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % proxies)
# browser = webdriver.Chrome(chrome_options=browser)
# browser.get("http://www.baidu.com")
# browser.find_element_by_id('kw').send_keys('IP')
# browser.find_element_by_id('su').click()


# 访问查询经纬度的网页exe
def get_page(mydb, addr):
    base_url = 'http://www.gpsspg.com/latitude-and-longitude.htm'
    browser.get(base_url)
    browser.find_element_by_id('u_text').send_keys(addr)
    browser.find_element_by_id('b_to').click()
    time.sleep(5)
    html = browser.page_source
    html = etree.HTML(html)
    print(html)
    jwd = html.xpath('//table[@id="table_list"]//tr/td/text()')
    if len(jwd) == 6:
        jd = float(jwd[1].split(',')[0])
        wd = float(jwd[1].split(',')[1])
        print(jd, wd)
        # 查重
        sql = 'select house_url from fang_xa'
        house_url = mydb.query(sql)
        for url in house_url:
            # sql = 'insert into fang_xa(jd, wd) values("%10g", "%10g")' % (jd, wd)
            sql = 'update fang_xa set jd="%f",wd="%f" where house_url="%s"' % (jd, wd, url)
            # sql = 'insert into fang_xa(jd, wd) values("1.2", "3.4")'
            print('执行向数据库中插入数据', url)
            mydb.exec(sql)


# 获取经纬度
def get_jwd(mydb):
    # 从数据库中获取房源地址
    sql = 'select house_addr from fang_xa'
    house_addr = mydb.query(sql)

    for addr in house_addr:
        # time.sleep(2)
        # for url in house_url:
            # sql = 'select jd from fang_xa where house_url = "%s"' % url
            # jd = mydb.query(sql)
            # print(jd, type(jd))
            # if jd[0][0] == None:
            #     print(3333333333333333333333333333333)
        addr = '北京' + addr[0]
        # get_page(mydb, addr, url)
        get_page(mydb, addr)
            # elif jd[0][0] == 0.0:
            #     print(4444444444444444444444444444444)
            #     addr = '北京' + addr[0]
            #     get_page(mydb, addr, url)
            # else:
            #     print(5555555555555555555555555555555)
            #     pass


if __name__ == '__main__':
    mydb = MySql('127.0.0.1', 'root', '1234qwer', 'mydb_qiji', 3306, 'utf8')
    get_jwd(mydb)


# # 循环输出26个英文小写字母
# import string
# wList = []
# for word in string.ascii_lowercase:
#     # wList.append(word)
#     print(word)
