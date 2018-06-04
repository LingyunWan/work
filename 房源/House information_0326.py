import requests
from lxml import etree
import IpProxyPool
import time
from numpy import random


# 替换数据中的换行符
def wrap(data):

    data = data.replace('\r\n', '').replace(' ', '')

    return data

def comma(data):

    if '，' in data:
        data = data.replace('，', ' ')
    elif ',' in data:
        data = data.replace(',', ' ')
    else:
        data = data

    return data

def parse_list(base_url):

    # 加载代理池
    proxies = IpProxyPool.get_proxy()
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
        #str1 = str0 + '//p[@class="title"]//text()'
        
        house_description = html.xpath(str0 + '//p[@class="title"]//text()')[0]
        house_description = comma(house_description)

        # 第二个分匹配规则(匹配房屋信息)
        #str2 = str0 + '//p[@class="mt12"]//text()'
        
        house = html.xpath(str0 + '//p[@class="mt12"]//text()')
        print(house, len(house))

        if len(house) == 7:

            # 调用函数
            room_num = wrap(house[0])
            room_num = comma(room_num)
            house_floor = wrap(house[2])
            house_floor = comma(house_floor)
            house_orientation = wrap(house[4])
            house_orientation = comma(house_orientation)
            architectural_age = wrap(house[6]).split('：')[1]
            print(room_num, house_floor, house_orientation, architectural_age)

        elif len(house) == 5:

            if u'室' not in house[0]:
                room_num = u'无'
                house_floor = wrap(house[0])
                house_orientation = wrap(house[2])
                architectural_age = wrap(house[4]).split('：')[1]
                print(room_num, house_floor, house_orientation, architectural_age)

            elif u'层' not in house[2]:
                room_num = wrap(house[0])
                house_floor = u'无'
                house_orientation = wrap(house[2])
                architectural_age = wrap(house[4]).split('：')[1]
                print(room_num, house_floor, house_orientation, architectural_age)

            elif u'向' not in house[4]:
                room_num = wrap(house[0])
                house_floor = wrap(house[2])
                house_orientation = u'无'
                architectural_age = wrap(house[4]).split('：')[1]
                print(room_num, house_floor, house_orientation, architectural_age)

            else:
                room_num = wrap(house[0])
                house_floor = wrap(house[2])
                house_orientation = wrap(house[4])
                architectural_age = u'无'
                print(room_num, house_floor, house_orientation, architectural_age)

        else:
            room_num = wrap(house[0])
            house_floor = wrap(house[2])
            house_orientation = u'无'
            architectural_age = u'无'
            print(room_num, house_floor, house_orientation, architectural_age)

        # 第三个分匹配规则(匹配房源信息)
        #str3 = str0 + '//p[@class="mt10"]//text()'
        
        addr = html.xpath(str0 + '//p[@class="mt10"]//text()')

        print(addr, len(addr))

        if len(addr) == 5:
            community_name = addr[1]
            house_address = addr[3]
            print(community_name, house_address )
            # 获得房子所属片区
            house_area = house_address.split("-")[0]
            house_addr = house_address.split("-")[1]
            print(house_area, house_addr )

        # 第四个分匹配规则(匹配附近地铁站)
        #str4 = str0 + '//div[contains(@class,"mt8")]//text()'
        
        subway = html.xpath(str0 + '//div[contains(@class,"mt8")]//text()')
        print(subway, len(subway))

        if len(subway) == 8:
            subway_name = subway[4]
            print(subway_name)
        elif len(subway) == 7:
            if u'满' in subway[3]:
                subway_name = u'无'
                print(subway_name )
            else:
                subway_name = subway[3]
                print(subway_name)
        elif len(subway) == 6:
            if u'满' in subway[2]:
                subway_name = u'无'
                print(subway_name)
            else:
                subway_name = subway[2]
                print(subway_name)
        else:
            subway_name = u'无'
            print(subway_name)
        subway_name = comma(subway_name)

        # 第五个分匹配规则(匹配房子建筑面积)
        str5 = str0 + '//div[contains(@class,"area")]//text()'
        area = html.xpath(str5)
        print(area, len(area))

        if len(area) == 5:
            building_area = area[1].replace('㎡', '')
            print('%s:' %area[3], building_area)

        # 第六个分匹配规则(匹配房子价格)
        #str6 = str0 + '//div[@class="moreInfo"]//text()'
        
        price = html.xpath(str0 + '//div[@class="moreInfo"]//text()')
        print(price, len(price))

        if len(price) == 8:
            setof_price = price[1]
            avg_price = price[4].replace(u'元', '')
            print(setof_price, avg_price)
            # print(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)
            with open('house_list1.csv', 'a+', encoding='gbk') as f:
                f.writelines(','.join([house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price, '\n']))
                f.close()


# 构建分页请求,分页获取房源信息
def getPage():

    for page_num in range(1, 11):

        base_url = 'http://esf.fang.com/house/i3%d/' % page_num
        print(base_url)
        time.sleep(random.randint(2, 6, random.randint(1, 2)))
        # time.sleep(1)
        parse_list(base_url)


if __name__ == '__main__':
    starttime = time.time()
    getPage()
    endtime = time.time()
    print(endtime - starttime)
    # parse_list()
