import requests
from lxml import etree
import string
import IpProxyPool
import time
from numpy import random
from MySql import MySql


# 替换数据中的换行符
def wrap(data):
    data = data.replace('\r\n', '').replace(' ', '')
    return data


# 替换数据中的逗号
def comma(data):
    if '，' in data:
        data = data.replace('，', ' ')
    elif ',' in data:
        data = data.replace(',', ' ')
    elif '元' in data:
        data = data.replace('元/平米', '')
    else:
        data = data.replace('平米', '')
    return data


# 判断数据是否存在
def exist(data):
    if data:
        data = data[0]
    else:
        data = ''
    return data



# 加载代理池
proxies = IpProxyPool.get_proxy()
# 调用代理IP
proxy = random.choice(proxies)


# 构建user_agent
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    'User-Agent': '%s' % random.choice(user_agent_list),
}


# 解析详情页
def parse_detail(url):

    req = requests.get(url, headers=headers, proxies=proxy)
    html = req.content.decode('utf-8')
    html = etree.HTML(html)
    # print(html)
    house_url = url
    title = html.xpath('//div[@id="lpname"]/div[1]/text()')
    title = wrap(exist(title))
    setof_price = html.xpath('//div[@class="trl-item_top"]/div/i/text()')
    setof_price = int(setof_price[0])
    layout = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][2]/div[contains(@class,"w146")]/div[1]/text()')
    layout = wrap(exist(layout))
    building_area = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][2]/div[contains(@class,"w182")]/div[1]/text()')
    building_area = float(comma(building_area[0]))
    unit_price = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][2]/div[contains(@class,"w132")]/div[1]/text()')
    unit_price = int(comma(unit_price[0]))
    orientation = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][3]/div[contains(@class,"w146")]/div[1]/text()')
    orientation = exist(orientation)
    floor = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][3]/div[contains(@class,"w182")]/div/text()')
    floor = ','.join(floor)
    residential = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][4]/div[contains(@class,"trl-item2")][1]//a[1]/text()')
    residential = exist(residential)
    region = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][4]/div[contains(@class,"trl-item2")][2]//a/text()')
    region = wrap(''.join(region))
    subway = html.xpath(
        '//div[@class="tab-cont-right"]/div[contains(@class,"tr-line")][4]/div[contains(@class,"trl-item2")][1]//span/text()')
    subway = exist(subway)
    print(house_url, title, setof_price, layout, building_area, unit_price, orientation, floor, residential, region,
          subway)
    # sql1 = 'select * from fang_xa where house_url="%s"' % house_url
    # sql2 = 'insert into fang_xa(house_url, title, setof_price, layout, building_area, unit_price, orientation, floor, residential, region, subway)' \
    #       'values("%s", "%s", "%d", "%s", "%f", "%d", "%s", "%s", "%s", "%s")' \
    #        % (house_url, title, setof_price, layout, building_area, unit_price, orientation, floor, residential, region, subway)
    # mydb.exe(sql1, sql2)


# 解析列表页
def parse_list(base_url, mydb):

        req = requests.get(base_url, headers=headers, proxies=proxy)
        html = req.content.decode('gbk')
        html = etree.HTML(html)
        house_url = html.xpath('//p[@class="title"]/a/@href')
        for url in house_url:
            # 构建详情页完整链接
            detail_url = 'http://esf.fang.com' + url
            # 解析详情页(需要获取详情页的页面链接)
            parse_detail(detail_url)

            # j = 0
        # # 匹配规则不完整,需要组合,得到的str0是所需的整体匹配规则
        # for i in range(30):
        #     if i < 9:
        #         lists = str(0) + str(i+1)
        #         str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + lists + '"]'
        #     else:
        #         str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + str(i+1) + '"]'

            # # 第一部分匹配规则(匹配title)
            # str1 = str0 + '//p[@class="title"]//text()'
            # str2 = str0 + '//p[@class="title"]/a/@href'
            # house_description = html.xpath(str1)
            # if house_description:
            #     house_description = comma(house_description[0])
            #     # /chushou/3_401622944.htm  匹配详情页链接(用于去重)
            #     house_url = 'http://esf.fang.com'+html.xpath(str2)[0]
            #     print(house_url)
            # else:
            #     house_description = ''
            #     house_url = '%d' % j
            #     j += 1
            # # 第二部分匹配规则(匹配房屋信息)
            # str2 = str0 + '//p[@class="mt12"]//text()'
            # house = html.xpath(str2)
            # if len(house) == 7:
            #     # 调用函数
            #     room_num = wrap(house[0])
            #     house_floor = wrap(house[2])
            #     house_orientation = wrap(house[4])
            #     architectural_age = wrap(house[6]).split('：')[1]
            #     architectural_age = int(architectural_age)
            # elif len(house) == 5:
            #     if '室' not in house[0]:
            #         # 调用函数
            #         room_num = ''
            #         house_floor = wrap(house[0])
            #         house_orientation = wrap(house[2])
            #         architectural_age = wrap(house[4]).split('：')[1]
            #         architectural_age = int(architectural_age)
            #
            #     elif '层' not in house[2]:
            #         # 调用函数
            #         room_num = wrap(house[0])
            #         house_floor = ''
            #         house_orientation = wrap(house[2])
            #         architectural_age = wrap(house[4]).split('：')[1]
            #         architectural_age = int(architectural_age)
            #     elif '向' not in house[4]:
            #         # 调用函数
            #         room_num = wrap(house[0])
            #         house_floor = wrap(house[2])
            #         house_orientation = ''
            #         architectural_age = wrap(house[4]).split('：')[1]
            #         architectural_age = int(architectural_age)
            #     else:
            #         # 调用函数
            #         room_num = wrap(house[0])
            #         house_floor = wrap(house[2])
            #         house_orientation = wrap(house[4])
            #         architectural_age = 0
            # else:
            #     # 调用函数
            #     room_num = wrap(house[0])
            #     house_floor = wrap(house[2])
            #     house_orientation = ''
            #     architectural_age = 0
            # room_num = comma(room_num)
            # house_floor = comma(house_floor)
            # house_orientation = comma(house_orientation)
            #
            # # 第三部分匹配规则(匹配房源信息)
            # str3 = str0 + '//p[@class="mt10"]//text()'
            # addr = html.xpath(str3)
            #
            # if len(addr) == 5:
            #     community_name = addr[1]
            #     house_address = addr[3]
            #     # 获得房子所属片区
            #     house_area = house_address.split("-")[0]
            #     house_addr = house_address.split("-")[1]
            #     house_area = comma(house_area)
            #     house_addr = comma(house_addr)
            #
            # # 第四部分匹配规则(匹配附近地铁站)
            # str4 = str0 + '//div[contains(@class,"mt8")]//text()'
            # subway = html.xpath(str4)
            #
            # if len(subway) == 8:
            #     subway_name = subway[4]
            # elif len(subway) == 7:
            #     if '满' in subway[3]:
            #         subway_name = ''
            #     else:
            #         subway_name = subway[3]
            # elif len(subway) == 6:
            #     if '满' in subway[2]:
            #         subway_name = ''
            #     else:
            #         subway_name = subway[2]
            # else:
            #     subway_name = ''
            # subway_name = comma(subway_name)
            #
            # # 第五部分匹配规则(匹配房子建筑面积)
            # str5 = str0 + '//div[contains(@class,"area")]//text()'
            # area = html.xpath(str5)
            #
            # if len(area) == 5:
            #     building_area = area[1].replace('㎡', '')
            #     building_area = int(building_area)
            #
            # # 第六部分匹配规则(匹配房子价格)
            # str6 = str0 + '//div[@class="moreInfo"]//text()'
            # price = html.xpath(str6)
            #
            # if len(price) == 8:
            #     setof_price = price[1]
            #     setof_price = round(float(setof_price))
            #     avg_price = price[4].replace('元', '')
            #     avg_price = int(avg_price)
            #
            # # 向mysql中进行存储
            # # print(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)
            # sql1 = 'select * from fang_xa where house_url="%s"' % house_url
            # sql2 = 'insert into fang_xa(house_url, house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)' \
            #       'values("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%d", "%d", "%d")' \
            #        % (house_url, house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)
            # mydb.exe(sql1, sql2)


# 构建分页请求,分页获取房源信息
def get_page():

    # 循环输出26个英文小写字母
    for letter in string.ascii_lowercase:
        # print(letter)
        for page_num in range(1, 101):
            base_url = 'http://esf.fang.com/house/%s3%d/'
            full_url = base_url % (letter, page_num)
            print(full_url)
            time.sleep(1)
            # time.sleep(random.randint(2, 6, random.randint(1, 2)))
            parse_list(full_url, mydb)


if __name__ == '__main__':
    starttime = time.time()
    # mydb = MySql('127.0.0.1', 'root', '1234qwer', 'mydb_qiji', 3306, 'utf8')
    mydb = MySql('127.0.0.1', 'root', '1234qwer', 'mysql_xa', 3306, 'utf8')
    get_page()
    endtime = time.time()
    print(endtime - starttime)
