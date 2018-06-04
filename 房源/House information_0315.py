import requests
from lxml import etree
import IpProxyPool
import time
from numpy import random

import re
import sys, urllib
from urllib import request
# reload(sys)
# sys.setdefaultencoding("utf-8")


def func(data):
    data = data.replace('\r\n', '').replace(' ', '')
    return data


# 加载代理池
proxies = IpProxyPool.get_proxy()



def parse_list(base_url):
    # print('crawling page %s' % base_url)
    # 起始路径
    # base_url = 'http://esf.fang.com/house/i32'
    # headers = {
    #     "Host": " esf.fang.com",
    #     "Connection": " keep-alive",
    #     "Cache-Control": " max-age=0",
    #     "Upgrade-Insecure-Requests": " 1",
    #     "User-Agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    #     "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     # "Accept-Encoding": " gzip, deflate",
    #     "Accept-Language": " zh-CN,zh;q=0.9",
    #     "Cookie": " global_cookie=1wysgftaj1tuy2c07iggpshp11cjenkx4zg; Integrateactivity=notincludemc; polling_imei=10c8e1ac180e2778; searchLabelN=1_1520822023_1629%5B%3A%7C%40%7C%3A%5Dc0f11b15b36d090f590355a37adb39b2; searchConN=1_1520822023_1726%5B%3A%7C%40%7C%3A%5D79f135e8e03904b34ebc1e4e8637aad5; budgetLayer=1%7Cbj%7C2018-03-12%2014%3A17%3A36; lastscanpage=0; SoufunSessionID_Esf=1_1520835456_4977; city=www; vh_newhouse=1_1520837401_977%5B%3A%7C%40%7C%3A%5Df89462600c08a631cca518a9c8bdf848; newhouse_user_guid=0925F7A3-98C9-93C0-C944-242C5519F16F; __utmz=147393320.1520837561.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=147393320; __utma=147393320.1539925281.1520819931.1521163844.1521167206.14; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.12.10.1521167206; unique_cookie=U_ovyn51v6tjs05nwnz3l61woqk2sjet9oe61*5",
    #
    # }
    # 发送http请求,获得响应(使用request)
    # req = request.Request(base_url)
    # 解析html页面,使用的是gbk格式
    # response = request.urlopen(req)
    # html = response.read().decode('gb2312')
    # get_ip_list = myproxy.getOpener(proxies)
    # 调用代理IP
    proxy = random.choice(proxies)
    print(proxy)
    req = requests.get(base_url, proxies=proxy)
    html = req.content.decode('gbk')
    html = etree.HTML(html)
    print(html)
    # 匹配规则不完整,需要组合,得到的str0是所需的整体匹配规则
    for i in range(30):
        if i < 9:
            lists = str(0) + str(i+1)
            str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + lists + '"]'
        else:
            str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + str(i+1) + '"]'
        # 第一个分匹配规则(匹配title)
        str1 = str0 + '//p[@class="title"]//text()'
        # print(str1, type(str1))
        # title = html.xpath('//div[@class="houseList"]/dl[@id="list_D03_01"]//p[@class="title"]//text()')[0]
        house_description = html.xpath(str1)[0]
        # print(house_description)
        # 第二个分匹配规则(匹配房屋信息)
        str2 = str0 + '//p[@class="mt12"]//text()'
        house = html.xpath(str2)
        # print(house)
        # print(len(house))
        if len(house) == 7:
            # room_num = house[0].replace('\r\n', '').replace(' ', '')
            # house_floor = house[2].replace('\r\n', '').replace(' ', '')
            # house_orientation = house[4].replace('\r\n', '').replace(' ', '')
            # architectural_age = house[6].replace('\r\n', '').replace(' ', '')
            # 调用函数
            room_num = func(house[0])
            house_floor = func(house[2])
            house_orientation = func(house[4])
            architectural_age = func(house[6])
            # room_num = re.sub('[\r\n]+', '', house[0])
            # print(room_num, house_floor, house_orientation, architectural_age)
        elif len(house) == 5:
            if '室' not in house[0]:
                # 调用函数
                room_num = ''
                house_floor = func(house[0])
                house_orientation = func(house[2])
                architectural_age = func(house[4])
                # print(room_num, house_floor, house_orientation, architectural_age)
            elif '层' not in house[2]:
                # 调用函数
                room_num = func(house[0])
                house_floor = ''
                house_orientation = func(house[2])
                architectural_age = func(house[4])
                # print(room_num, house_floor, house_orientation, architectural_age)
            elif '向' not in house[4]:
                # 调用函数
                room_num = func(house[0])
                house_floor = func(house[2])
                house_orientation = ''
                architectural_age = func(house[4])
                # print(room_num, house_floor, house_orientation, architectural_age)
            else:
                # 调用函数
                room_num = func(house[0])
                house_floor = func(house[2])
                house_orientation = func(house[4])
                architectural_age = ''
                # print(room_num, house_floor, house_orientation, architectural_age)
        else:
            # 调用函数
            room_num = func(house[0])
            house_floor = func(house[2])
            house_orientation = ''
            architectural_age = ''
        # 第三个分匹配规则(匹配房源信息)
        str3 = str0 + '//p[@class="mt10"]//text()'
        addr = html.xpath(str3)
        # print(addr)
        # print(len(addr))
        if len(addr) == 5:
            community_name = addr[1]
            house_address = addr[3]
            # print(community_name, house_address)
            # 获得房子所属片区
            house_area = house_address.split("-")[0]
            house_addr = house_address.split("-")[1]
            # print(house_area)
        # 第四个分匹配规则(匹配附近地铁站)
        str4 = str0 + '//div[contains(@class,"mt8")]//text()'
        subway = html.xpath(str4)
        # print(subway_name)
        # print(len(subway_name))
        if len(subway) == 8:
            subway_name = subway[4]
            # print(subway_name)
        elif len(subway) == 7:
            if '满' in subway[3]:
                subway_name = ''
                # print(subway_name)
            else:
                subway_name = subway[3]
                # print(subway_name)
        elif len(subway) == 6:
            if '满' in subway[2]:
                subway_name = ''
                # print(subway_name)
            else:
                subway_name = subway[2]
                # print(subway_name)
        else:
            subway_name = ''
            # print(subway_name)
        # 第五个分匹配规则(匹配房子建筑面积)
        str5 = str0 + '//div[contains(@class,"area")]//text()'
        area = html.xpath(str5)
        # print(area)
        # print(len(area))
        if len(area) == 5:
            building_area = area[1]
            # print('%s:' %area[3], building_area)
        # 第六个分匹配规则(匹配房子价格)
        str6 = str0 + '//div[@class="moreInfo"]//text()'
        price = html.xpath(str6)
        # print(price)
        # print(len(price))
        if len(price) == 8:
            setof_price = price[1]
            avg_price = price[4]
            # print(setof_price, avg_price)
        # print(house_description, room_num, house_floor, house_orientation, architectural_age.split('：')[1], community_name, house_area, house_addr, subway_name, building_area.replace('㎡', ''), setof_price, avg_price.replace('元', ''))
            # print(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, subway_name, setof_price, avg_price)
        with open('house_list.csv', 'a+', encoding='utf-8') as f:
            # f.write(house_description, room_num, house_floor, house_orientation, architectural_age.split('：')[1], community_name, house_area, house_addr, subway_name, building_area.replace('㎡', ''), setof_price, avg_price.replace('元', ''))
            f.writelines(','.join([house_description, room_num, house_floor, house_orientation, architectural_age.split('：')[1], community_name, house_area, house_addr, subway_name, building_area.replace('㎡', ''), setof_price, avg_price.replace('元', ''), '\n']))
        #     # pass
            f.close()


# 构建分页请求,分页获取房源信息
def getPage():
    for page_num in range(1, 2):
        base_url = 'http://esf.fang.com/house/i3%d'
        full_url = base_url % page_num
        print(full_url)
        # time.sleep(random.randint(2,6,random.randint(1,2)))
        time.sleep(1)
        parse_list(full_url)


if __name__ == '__main__':
    getPage()
    # parse_list()

    # 房天下获取验证码的网址
    # http://search.fang.com/captcha-verify/?t=1521450215.945&h=aHR0cDovL2VzZi5mYW5nLmNvbS9ob3VzZS9pMzE%3D&c=cmE6MTA2LjM3LjEwMi4xODY7eHJpOjt4ZmY6
