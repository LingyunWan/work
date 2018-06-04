# with open('../get_ip_list', 'r+') as f:
#     print(f.readlines())
# print('%s','%s','%s')
# print(round(str(93.9)))
# import string
#
# # for word in string.ascii_lowercase:
# for word in string.ascii_letters:
#     with open('1.txt', 'r+') as f:
#         words = f.readlines()
#         # print(words)
#         word = word + '\n'
#         if word in words:
#             print('存在')
#         else:
#             print('不存在')
#             f.write(word)
#
# with open('get_ip_list', 'r+') as f:
#     # f.write(word+'\n')
#     # f.close()
#     words = f.readlines()
#     print(words)
#     ip = '115.46.67.219'
#     port  = '8123'
#     contype = 'HTTP'
#     ip = ' '.join([ip, port, contype]) + '\n'
#     # ip = ip
#     # ip = ip+' '+port+' '+contype+'\n'
#     print('%s' % ip)
#     if ip in words:
#         print(1)
#     else:
#         print(2)
#
# import string
#
# # for word in string.ascii_lowercase:
# for word in string.ascii_letters:
#     f = open('2.txt', 'a+')
#     f.write(word)
with open('../get_ip_list', 'r') as f:
    ips = f.readlines()
    print(ips)
    for ip in ips:
        # print(ip)
        with open('../ip_list', 'r+') as fl:
            ip_lists = fl.readlines()
            print(ip_lists)
            if ip in ip_lists:
                print('重复')
            else:
                fl.write(ip)
