# coding=UTF-8
import urllib.request
import chardet
import requests
import time

import IpProxyPool


# 加载代理池
proxies = IpProxyPool.get_proxy()
print(proxies)


def url_user_agent():
    # url = 'http://quote.stockstar.com/stock'
    base_url = 'http://www.baidu.com/'

    # inFile = open('get_ip_list', 'r')
    # f = open("get_ip", "wb")

    for proxy in proxies:
        time.sleep(3)
        # req = requests.get(base_url, proxies=proxy)
        # html = req.content.decode('utf-8')
        # print(html)
        # html = etree.HTML(html)



    # for line in inFile.readlines():
        # f.write(line+'\n')

        # print(line)
        # line = line.strip('\n')
        # # proxy_host = '://'.join(line.split('='))
        # proxy_host = line.split('=')[1]
        # # print(proxy_host)
        # proxy_temp = {line.split("=")[0]: proxy_host}
        # print(proxy_temp)

        # proxy_temp = {'http':'58.33.37.205:8118'}
        # 设置使用代理
        # proxy_temp = {'http':'119.5.0.100:808'}
        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler(debuglevel=1))
        opener = urllib.request.build_opener(proxy_support)
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows N/T 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
        req = urllib.request.Request(base_url,headers=i_headers)
        opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")]

        urllib.request.install_opener(opener)

        # 添加头信息，模仿浏览器抓取网页，对付返回403禁止访问的问题
        # i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        try:
            html = urllib.request.urlopen(base_url, timeout=5)
            content = html.read()
            print(content)
            # print(type(content))
            # print(chardet.detect(content))
            print("==============================")
            if content.strip() != '':
                print(proxy['https'], type(proxy['https']))
                proxy = proxy['https'] + '\n'
                # 如果是存储为txt格式的,就需要进行编码
                # data = proxy.encode(encoding="UTF-8")
                with open('get_ip', 'a+') as f:
                    print(111111111111111111111)
                    f.write(proxy)

        except Exception as e:
            # print('%s connect failed' % line)
            print('连接失败')

    f.close()
    print("Test End !")


if __name__ == '__main__':
    # pass
    url_user_agent()
