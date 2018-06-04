import random
import re
import requests
import time


# 加载代理池
import IpProxyPool


class IPProxyPool:
    def __init__(self):
        self.ip_list = []
        self.user_agent_list = [
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

    def parse_list(self, ip_url='http://www.xicidaili.com/nn'):
        # 调用代理IP
        proxies = IpProxyPool.get_proxy()
        proxy = random.choice(proxies)
        print(proxy)
        # 访问西刺代理网站,来获取免费可用代理
        # req = requests.get(ip_url)
        headers = {
            'User-Agent': '%s' % self.user_agent_list,
        }
        # headers = random.choice(self.user_agent_list)
        # code = requests.get(ip_url, proxies=proxy, headers=headers).status_code
        # print(code)
        req = requests.get(ip_url, headers=headers, proxies=proxy)
        html = req.content.decode('utf-8')
        # print(html)
        tr_pattern = re.compile(r'<tr.*?>.*?</tr>', re.S)  # re.S让.可以匹配换行
        tr_list = tr_pattern.findall(html)[1:]

        # with open('get_ip_list', 'r+', encoding='utf-8') as f:
        for tr in tr_list:
            td_pattern = re.compile('<td>(.*?)</td>')
            info_pattern = re.compile(r'title="(.*?)".*?title="(.*?)"', re.S)
            td_list = td_pattern.findall(tr)
            info_list = info_pattern.findall(tr)
            info_list = info_list[0]

            speed = info_list[0]  # 获取连接速度
            speed = speed.replace('秒', '')

            contime = info_list[1]  # 获取连接时间
            contime = contime.replace('秒', '')

            ip = td_list[0]
            port = td_list[1]
            contype = td_list[2]
            alive = td_list[3]
            if float(speed) < 1:  # 过滤速度
                if float(contime) < 1:  # 过滤连接时间
                    if '天' in alive:  # 过滤存活时间
                        alive = alive.replace('天', '')
                        if int(alive) > 10:
                            print(ip, port, contype, alive, speed, contime)
                            proxies = []
                            proxy = {}  # 代理字典
                            proxy[contype] = contype + '://' + ip + ':' + port
                            proxies.append(proxy)
                            # get_ip_list = random.choice(proxies)  # 随机选择代理池proies中的一个代理
                            # 检测获取到的代理是否能用
                            for proxy in proxies:
                                print(proxy)
                                base_url = 'https://www.baidu.com/'
                                # 验证爬取的IP是否可用(通过访问百度的状态码来判断)
                                # 使用urllib时状态码获取是 .code , 而使用requests是 .status_code
                                # code = requests.get(ip_url, proxies=proxy, headers=headers).status_code
                                code = requests.get(base_url, proxies=proxy, headers=headers).status_code
                                proies = []
                                print(code)
                                if code == 200:    # 如果能正常访问百度,即可用IP,就存储到文件中
                                    proies.append(proxy)
                                    with open ('get_ip_list', 'r+') as f:
                                        ips = f.readlines()
                                        ip = ' '.join([ip, port, contype]) + '\n'
                                        if ip in ips:
                                            print('重复')
                                        else:
                                            print('不重复')
                                            f.write(ip)
                                            f.close()
                                else:   # 若不能正常访问百度,则直接pass
                                    pass

    # 构建分页请求
    def getPage(self):
        start = input('输入起始页:')
        end = input('输入结束页:')
        # 构建分页请求路径
        for page in range(int(start), int(end) + 1):
            base_url = 'http://www.xicidaili.com/nn/%d'
            fullurl = base_url % page
            time.sleep(random.randint(1, 6))
            self.parse_list(fullurl)


IPProxyPool = IPProxyPool()
IPProxyPool.getPage()
