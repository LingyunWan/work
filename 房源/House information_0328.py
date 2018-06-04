import pymysql
import requests
from lxml import etree
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
    else:
        data = data
    return data


# 加载代理池
proxies = IpProxyPool.get_proxy()


# def parse_list(base_url, mydb):
def parse_list(base_url):

        # 调用代理IP
        proxy = random.choice(proxies)
        print(proxy)
        req = requests.get(base_url, proxies=proxy)
        html = req.content.decode('gbk')
        html = etree.HTML(html)
        # print(html)
        # 匹配规则不完整,需要组合,得到的str0是所需的整体匹配规则
        for i in range(30):
            if i < 9:
                lists = str(0) + str(i+1)
                str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + lists + '"]'
            else:
                str0 = '//div[@class="houseList"]/dl[@id="list_D03_' + str(i+1) + '"]'

            # # 存储到数据库中
            try:
                # 连接数据库
                conn = pymysql.connect('127.0.0.1', 'root', '1234qwer', 'mydb_qiji', charset='utf8')
                # 创建数据库操作的游标
                cursor = conn.cursor()
                #     sql = 'insert into fang_xa(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)' \
                #           'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)'

                # 第一部分匹配规则(匹配title)
                str1 = str0 + '//p[@class="title"]//text()'
                house_description = html.xpath(str1)[0]
                house_description = comma(house_description)
                # print(house_description)
                # sql = 'insert into fang_xa(house_description) values("%s")' % house_description
                # mydb.exe(sql)
                # 第二部分匹配规则(匹配房屋信息)
                str2 = str0 + '//p[@class="mt12"]//text()'
                house = html.xpath(str2)
                # print(house)
                # print(len(house))

                if len(house) == 7:
                    # 调用函数
                    room_num = wrap(house[0])
                    house_floor = wrap(house[2])
                    house_orientation = wrap(house[4])
                    architectural_age = wrap(house[6]).split('：')[1]
                    architectural_age = int(architectural_age)
                    # print(room_num, house_floor, house_orientation, architectural_age)
                elif len(house) == 5:
                    if '室' not in house[0]:
                        # 调用函数
                        room_num = '无'
                        house_floor = wrap(house[0])
                        house_orientation = wrap(house[2])
                        architectural_age = wrap(house[4]).split('：')[1]
                        architectural_age = int(architectural_age)
                        # print(room_num, house_floor, house_orientation, architectural_age)
                    elif '层' not in house[2]:
                        # 调用函数
                        room_num = wrap(house[0])
                        house_floor = '无'
                        house_orientation = wrap(house[2])
                        architectural_age = wrap(house[4]).split('：')[1]
                        architectural_age = int(architectural_age)
                        # print(room_num, house_floor, house_orientation, architectural_age)
                    elif '向' not in house[4]:
                        # 调用函数
                        room_num = wrap(house[0])
                        house_floor = wrap(house[2])
                        house_orientation = '无'
                        architectural_age = wrap(house[4]).split('：')[1]
                        architectural_age = int(architectural_age)
                        # print(room_num, house_floor, house_orientation, architectural_age)
                    else:
                        # 调用函数
                        room_num = wrap(house[0])
                        house_floor = wrap(house[2])
                        house_orientation = wrap(house[4])
                        architectural_age = 0
                        # print(room_num, house_floor, house_orientation, architectural_age)
                else:
                    # 调用函数
                    room_num = wrap(house[0])
                    house_floor = wrap(house[2])
                    house_orientation = '无'
                    architectural_age = 0
                    # print(room_num, house_floor, house_orientation, architectural_age)
                room_num = comma(room_num)
                house_floor = comma(house_floor)
                house_orientation = comma(house_orientation)
                # 第三部分匹配规则(匹配房源信息)
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
                    # print(house_area, house_addr)
                    house_area = comma(house_area)
                    house_addr = comma(house_addr)
                # 第四部分匹配规则(匹配附近地铁站)
                str4 = str0 + '//div[contains(@class,"mt8")]//text()'
                subway = html.xpath(str4)
                # print(subway)
                # print(len(subway))
                if len(subway) == 8:
                    subway_name = subway[4]
                    # print(subway_name)
                elif len(subway) == 7:
                    if '满' in subway[3]:
                        subway_name = '无'
                        # print(subway_name)
                    else:
                        subway_name = subway[3]
                        # print(subway_name)
                elif len(subway) == 6:
                    if '满' in subway[2]:
                        subway_name = '无'
                        # print(subway_name)
                    else:
                        subway_name = subway[2]
                        # print(subway_name)
                else:
                    subway_name = '无'
                    # print(subway_name)
                subway_name = comma(subway_name)
                # 第五部分匹配规则(匹配房子建筑面积)
                str5 = str0 + '//div[contains(@class,"area")]//text()'
                area = html.xpath(str5)
                # print(area)
                # print(len(area))
                if len(area) == 5:
                    building_area = area[1].replace('㎡', '')
                    building_area = int(building_area)
                    # print('%s:' % area[3], building_area)
                # 第六部分匹配规则(匹配房子价格)
                str6 = str0 + '//div[@class="moreInfo"]//text()'
                price = html.xpath(str6)
                # print(price)
                # print(len(price))
                if len(price) == 8:
                    setof_price = price[1]
                    setof_price = int(setof_price)
                    avg_price = price[4].replace('元', '')
                    avg_price = int(avg_price)
                    # print(setof_price, avg_price)
                    # 存储位csv文件
                    # with open('house_list.csv', 'a+', encoding='gbk') as f:
                    #     f.writelines(','.join([house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price, '\n']))
                    #     f.close()

                cursor.execute('insert into fang_xa(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)' \
                          'values(%s, %s, %s, %s, %d, %s, %s, %s, %s, %d, %d, %d,)') % (house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)
                # sql = 'insert into fang_xa(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price)' \
                #               'values(house_description, room_num, house_floor, house_orientation, int(architectural_age), community_name, house_area, house_addr, subway_name, int(building_area), int(setof_price), int(avg_price))'
                # mydb.exe(sql)
                # # 提交sql语句
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print('连接异常', str(e))


# 构建分页请求,分页获取房源信息
def get_page():
    for page_num in range(1, 2):
        base_url = 'http://esf.fang.com/house/i3%d/'
        full_url = base_url % page_num
        print(full_url)
        # time.sleep(1)
        time.sleep(random.randint(2, 6, random.randint(1, 2)))
        # parse_list(full_url, mydb)
        parse_list(full_url)


if __name__ == '__main__':
    starttime = time.time()
    # mydb = MySql('127.0.0.1', 'root', '1234qwer', 'mydb_qiji', 3306, 'utf8')
    get_page()
    endtime = time.time()
    print(endtime - starttime)
