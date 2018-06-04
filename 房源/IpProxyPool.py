from numpy import random
from urllib import request


def get_proxy():
    with open(r'get_ip_list', 'r') as f:
        proxy_list = f.readlines()  # 读取每一行
        proxies = []
        for pro in proxy_list:  # 循环获取代理信息，追加到列表中
            proxy_info = pro.replace('\n', '').split(' ')
            proies = {}  # 代理字典
            # get_ip_list['http'] = proxy_info[2] + '://' + proxy_info[0] + ':' + proxy_info[1]
            proies['https'] = proxy_info[2] + '://' + proxy_info[0] + ':' + proxy_info[1]
            proxies.append(proies)
            # proxy = random.choice(proxies)   # 随机选择代理池proies中的一个代理
    return proxies


# 使用urllib的时候需要下面几个步骤,而使用requests的时候则不用使用
# def getOpener(proxies):
    # proxy_handler = request.ProxyHandler(get_ip_list)  #
    # opener = request.build_opener(proxy_handler)
    # return opener
    # return proxy
