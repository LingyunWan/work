import time
from lxml import etree
from selenium import webdriver
from MySql import MySql


"""
from selenium import webdriver
 
PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
 
chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("http://whatismyipaddress.com")
"""

# 加载代理池
browser = webdriver.Chrome(executable_path=r"C:\Projects\virtualenv\python_03env\Scripts\chromedriver.exe")


# 访问获取经纬度的网站
def get_page(mydb):

    base_url = 'http://www.gpsspg.com/latitude-and-longitude.htm'
    browser.get(base_url)

    # 查重
    sql = 'select house_url from fang_xa'
    house_url = mydb.query(sql)

    count = 0   # 用于计算输入的需要查询的地址条数
    num = 0   # 用于计算数据库中总行数(由于是每输入十个数据查询一次)
    url_list = []   # 用于储存需要查询的地址相对应的路径
    ud_num = 0   # 用于计算向数据库中更新的经纬度次数

    time1 = time.time()
    for url in house_url:

        # 从数据库中获取经纬度状况
        sql = 'select jd from fang_xa where house_url="%s"' % url
        jd = mydb.query(sql)

        # 从数据库中获取房源所属小区
        sql = 'select house_area from fang_xa where house_url="%s"' % url
        house_area = mydb.query(sql)

        # 从数据库中获取房源所属小区
        sql = 'select community_name from fang_xa where house_url="%s"' % url
        community_name = mydb.query(sql)

        # 判断数据库中是否已经有经纬度
        if jd[0][0] is None:    # 还没有获取经纬度
            addr = '北京' + house_area[0][0] + community_name[0][0] + '\n'
            browser.find_element_by_id('u_text').send_keys(addr)
            time.sleep(2)
            count += 1
            num += 1
            url_list.append(url)

            # 如果输入的地址条数达到10条,就查询一次
            if num != len(house_url):

                if count != 0 and count % 10 == 0:
                    browser.find_element_by_id('b_to').click()
                    # 给予充分缓冲的时间(然后在获取页面信息)
                    print('2 * (time1 - time0)为', 20 * (time1 - time0))
                    if (time1 - time0) > 1.3 or (time1 - time0) < 1.2:
                        time.sleep(25)
                    # elif (time1 - time0) > 1.2:
                    #     time.sleep(25)
                    else:
                        time.sleep(20 * (time1 - time0))
                    html = browser.page_source
                    html = etree.HTML(html)
                    rwjd = html.xpath('//div[@id="b_st"]//span/text()')

                    if '就绪' in rwjd[0]:
                        # print('(time0 - time1) / 5为', (time1 - time0) / 5)
                        time.sleep((time1 - time0) / 5)
                        jwds = html.xpath('//table[@id="table_list"]//tr/td[2]/text()')
                        # print(jwds)
                        print('ud_num是', ud_num)
                        print('开始执行数据库的更新')

                        for j in range(10 * ud_num, count):

                            i = 3 * j
                            sql = 'update fang_xa set jd="%s",wd="%s" where house_url="%s"' % (
                                jwds[i].split(',')[0], jwds[i].split(',')[1], url_list[j][0])
                            # print(sql)
                            mydb.exec(sql)
                        ud_num += 1

                    else:
                        print('不执行更新数据库的操作')

            else:
                browser.find_element_by_id('b_to').click()
                # 给予充分缓冲的时间(然后在获取页面信息)
                # print('2 * (time1 - time0)为', 20 * (time1 - time0))
                time.sleep(20 * (time1 - time0))
                html = browser.page_source
                html = etree.HTML(html)
                rwjd = html.xpath('//div[@id="b_st"]//span/text()')

                if '就绪' in rwjd[0]:
                    # print('(time0 - time1) / 5为', (time1 - time0) / 5)
                    time.sleep((time1 - time0) / 5)
                    jwds = html.xpath('//table[@id="table_list"]//tr/td[2]/text()')
                    # print(jwds)
                    print('ud_num是', ud_num)
                    print('开始执行数据库的更新')

                    for j in range(10 * ud_num, count):

                        i = 3 * j
                        sql = 'update fang_xa set jd="%s",wd="%s" where house_url="%s"' % (
                            jwds[i].split(',')[0], jwds[i].split(',')[1], url_list[j][0])
                        # print(sql)
                        mydb.exec(sql)
                    ud_num += 1

                else:
                    print('不执行更新数据库的操作')
                    # time.sleep(count/10 - ud_num)

        # elif jd[0][0] == '0':   # 没有获取到经纬度
        #     addr = '北京' + house_area[0][0] + community_name[0][0] + '\n'
        #     browser.find_element_by_id('u_text').send_keys(addr)
        #     time.sleep(2)
        #     count += 1
        #     num += 1
        #     url_list.append(url)
        #
        #     # 判断数据库中所有房源路径是否已经全部查询
        #     if num != len(house_url):   # 没有全部查询
        #
        #         # 如果输入的地址条数达到10条,就查询一次
        #         if count != 0 and count % 10 == 0:
        #             browser.find_element_by_id('b_to').click()
        #             # 给予充分缓冲的时间(然后在获取页面信息)
        #             print('2 * (time1 - time0)为', 20 * (time1 - time0))
        #             time.sleep(20 * (time1 - time0))
        #             html = browser.page_source
        #             html = etree.HTML(html)
        #             rwjd = html.xpath('//div[@id="b_st"]//span/text()')
        #
        #             # 判断所有的地址对应的经纬度是否已经缓冲完成
        #             if '就绪' in rwjd[0]:
        #                 time.sleep((time1 - time0) / 5)
        #                 jwds = html.xpath('//table[@id="table_list"]//tr/td[2]/text()')
        #                 # print(jwds)
        #                 print('ud_num是', ud_num)
        #                 print('开始执行数据库的更新')
        #
        #                 # 把获取的经纬度更新到数据库中
        #                 for j in range(10 * ud_num, count):
        #                     i = 3 * j
        #                     sql = 'update fang_xa set jd="%s",wd="%s" where house_url="%s"' % (
        #                         jwds[i].split(',')[0], jwds[i].split(',')[1], url_list[j][0])
        #                     # print(sql)
        #                     mydb.exec(sql)
        #                 ud_num += 1
        #
        #             else:
        #                 print('不执行更新数据库的操作')
        #
        #     else:   # 已经全部查询过
        #         browser.find_element_by_id('b_to').click()
        #         # 给予充分缓冲的时间(然后在获取页面信息)
        #         # print('2 * (time1 - time0)为', 20 * (time1 - time0))
        #         time.sleep(20 * (time1 - time0))
        #         html = browser.page_source
        #         html = etree.HTML(html)
        #         rwjd = html.xpath('//div[@id="b_st"]//span/text()')
        #
        #         if '就绪' in rwjd[0]:
        #             # print('(time0 - time1) / 5为', (time1 - time0) / 5)
        #             time.sleep((time1 - time0) / 5)
        #             jwds = html.xpath('//table[@id="table_list"]//tr/td[2]/text()')
        #             # print(jwds)
        #             print('ud_num是', ud_num)
        #             print('开始执行数据库的更新')
        #
        #             for j in range(10 * ud_num, count):
        #                 # print('开始执行数据库的更新')
        #                 i = 3 * j
        #                 sql = 'update fang_xa set jd="%s",wd="%s" where house_url="%s"' % (
        #                     jwds[i].split(',')[0], jwds[i].split(',')[1], url_list[j][0])
        #                 # print(sql)
        #                 mydb.exec(sql)
        #             ud_num += 1
        #
        #         else:
        #             print('不执行更新数据库的操作')
        #             # time.sleep(count/10 - ud_num)

        else:   # 经纬度已经存在
            num += 1
            # html = browser.page_source
            # html = etree.HTML(html)
            # textarea = html.xpath('//textarea[@id="u_text"]')
            # print(textarea)
            # if num != len(house_url):
            #     pass
            # else:
            #     browser.find_element_by_id('b_to').click()
            #     # 给予充分缓冲的时间(然后在获取页面信息)
            #     print('2 * (time1 - time0)为', 20 * (time1 - time0))
            #     time.sleep(20 * (time1 - time0))
            #     html = browser.page_source
            #     html = etree.HTML(html)
            #     rwjd = html.xpath('//div[@id="b_st"]//span/text()')
            #
            #     if '就绪' in rwjd[0]:
            #         print('(time0 - time1) / 5为', (time1 - time0) / 5)
            #         time.sleep((time1 - time0) / 5)
            #         jwds = html.xpath('//table[@id="table_list"]//tr/td[2]/text()')
            #         print(jwds)
            #         print('ud_num是', ud_num)
            #
            #         for j in range(10 * ud_num, count):
            #             print('开始执行数据库的更新')
            #             i = 3 * j
            #             sql = 'update fang_xa set jd="%s",wd="%s" where house_url="%s"' % (
            #                 jwds[i].split(',')[0], jwds[i].split(',')[1], url_list[j][0])
            #             print(sql)
            #             mydb.exec(sql)
            #         ud_num += 1
            #
            #     else:
            #         print('不执行更新数据库的操作')


if __name__ == '__main__':
    time0 = time.time()
    myDb = MySql('127.0.0.1', 'root', '1234qwer', 'mydb_qiji', 3306, 'utf8')
    get_page(myDb)


# # 循环输出26个英文小写字母
# import string
# wList = []
# for word in string.ascii_lowercase:
#     # wList.append(word)
#     print(word)
