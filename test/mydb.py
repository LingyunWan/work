import pymysql

try:
    # 连接数据库host='localhost',user='root',  passwd='123456',port=3306, db='test01'
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234qwer', db='mydb_qiji', port=3306, charset='utf8')
    # 创建数据库操作的游标
    cursor = conn.cursor()
    # 创建数据库操作的游标
    cursor = conn.cursor()
    # cursor.execute('insert into fang_xa(house_description, room_num, house_floor, house_orientation, architectural_age, community_name, house_area, house_addr, subway_name, building_area, setof_price, avg_price) values(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)')
    # sql = 'insert into fang_xa(house_description, room_num) values("%s", "%s")' % ("无", "测试")
    sql = 'insert into fang_xa(house_description, room_num) values("无", "测试")'
    cursor.execute(sql)
    # 提交sql语句
    conn.commit()
    cursor.close()
    conn.close()
    print('连接正常')
except Exception as e:
    print('连接异常')
    print(str(e))
