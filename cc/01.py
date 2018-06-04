# from datetime import *
import time
#
#
# print(datetime.max)
# print(datetime.min)
# print(datetime.resolution)
# print(datetime.today())
# print(datetime.now())
# print(datetime.utcnow())
# print(datetime.fromtimestamp(time.time()))
# print(datetime.utcfromtimestamp(time.time()))
#
# d = date(2012, 9, 12)
# from  datetime  import  *
# t = time(19, 46, 5)
# print(datetime.combine(d, t))
# datetime = datetime.combine(d, t)
# print(datetime.strftime("2012-09-12 21:08:12"))
#
# dt = datetime.strptime("2012-09-12 21:08:12", "%Y-%m-%d %H:%M:%S")
# #print: 2012 9 12 21 8 12 0 None
# print(dt.year)
# print(dt.month)
# print(dt.day)
# print(dt.hour)
# print(dt.minute)
# print(dt.second)
# print(dt.microsecond)
# print(dt.tzinfo)
# print (dt.date())
# print (dt.time())
# print (dt.replace(year = 2013))
# print (dt.timetuple())
# print (dt.utctimetuple())
# print (dt.toordinal())
# print (dt.weekday())
# print (dt.isocalendar())
#
#
# # inputtime = input('请输入日期时间(格式:xxxx-xx-xx xx:xx:xx)')
# # dt = datetime.strptime(inputtime, "%Y-%m-%d %H:%M:%S")
# # hour = dt.hour
# # minute = dt.minute
# #
# # if hour == 00:
# #     li_min = [min for min in range(minute) if min % 5 == 0]
# #     for min in li_min:
# #         print(dt.replace(minute = min, second=0))
# # else:
# #     for hou in range(hour+1):
# #         if hou != hour:
# #             li_min = [min for min in range(60) if min % 5 == 0]
# #             for min in li_min:
# #                 print(dt.replace(hour=hou, minute=min, second=0))
# #             pass
# #         else:
# #             li_min = [min for min in range(minute) if min % 5 == 0]
# #             for min in li_min:
# #                 print(dt.replace(hour=hou, minute=min, second=0))
#
# # Publisher.objects.filter(country="U.S.A.", name__contains="press")
#
# # !/usr/bin/python
# # -*- coding: UTF-8 -*-
#
#
# import time
# import threading
# #
# # 为线程定义一个函数
# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#
#
# # 创建两个线程
# try:
#
#     threading._start_new_thread(print_time, ("Thread-1", 2,))
#     threading._start_new_thread(print_time, ("Thread-2", 4,))
#
# except:
#     print("Error: unable to start thread")
#
# while 1:
#     pass
#
#
# import time
#
# # localtime = time.localtime(time.time())
# # 获取格式化的时间time.ctime(second)或者time.asctime(tuple)
# # time.ctime(second)  括号里面的参数应该传秒数, 因此应该是整型
# # time.asctime(tuple)  括号里面的参数应该传元组
# # 两者格式化后的时间结果是一样的
# localtime = time.asctime(time.localtime(time.time()))
# print("本地时间为 :", localtime)
#
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#
# # 格式化成Sat Mar 28 22:24:24 2016形式
# print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
#
# # 将格式字符串转换为时间戳
# a = "Sat Mar 28 22:24:24 2016"
# print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))
#
#
# import calendar
#
# cal = calendar.month(2016, 1)
# print("以下输出2016年1月份的日历:")
# print(cal)


# 题目3
import threading


def save( num, data ):
    with open('file%d.dat' % num, 'a+', encoding='utf-8') as fl:
        fl.write(data)
        print('开始进行存储')
        # time.sleep(1)
        fl.close()


with open('file.dat', 'r', encoding='utf-8') as f:
    datas = f.readlines()   # 读取原文件中的所有数据

    for data in datas:
        num = int(data) * 1024 % 9

        # 线程一
        if num == 0:
            print('进入线程一')
            # threading._start_new_thread(save, (num, data, ))
            t0 = threading.Thread(target=save, args=(num, data, ))
            '''
            模块threading中的Thread方法 , 可以携带的参数有(target=save, args=(num, data, ))
            其中target是调用的函数 , args是调用该函数需要传入的参数。
            '''
            t0.start()
            '''
            join的作用是保证当前线程执行完成后，再执行其它线程。
            join可以有timeout参数，表示阻塞其它线程timeout秒后，不再阻塞。
            注释掉join , 就有可能是运行了多个线程 , 打印出了多个'进入线程X' , 之后才输出一个'开始进行存储'。
            有join的情况下 , 是输出一个'进入线程X' , 就输出一个'开始进行存储' , 之后交替输出。
            '''
            t0.join()

        # 线程一
        elif num == 1:
            t1 = threading.Thread(target=save, args=(num, data,))
            t1.start()
            t1.join()
            print('进入线程二')
        elif num == 2:
            t2 = threading.Thread(target=save, args=(num, data,))
            t2.start()
            t2.join()
            print('进入线程三')
        elif num == 3:
            t3 = threading.Thread(target=save, args=(num, data,))
            t3.start()
            t3.join()
            print('进入线程四')
        elif num == 4:
            t4 = threading.Thread(target=save, args=(num, data,))
            t4.start()
            t4.join()
            print('进入线程五')
        elif num == 5:
            t5 = threading.Thread(target=save, args=(num, data,))
            t5.start()
            t5.join()
            print('进入线程六')
        elif num == 6:
            t6 = threading.Thread(target=save, args=(num, data,))
            t6.start()
            t6.join()
            print('进入线程七')
        elif num == 7:
            t7 = threading.Thread(target=save, args=(num, data,))
            t7.start()
            t7.join()
            print('进入线程八')
        else:
            t8 = threading.Thread(target=save, args=(num, data,))
            t8.start()
            t8.join()
            print('进入线程九')
