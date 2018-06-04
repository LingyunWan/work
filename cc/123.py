import requests
from urllib import request
from lxml import etree
import re
import pymysql
import time
import json


# QQ音乐
song_id = '212841502'  # 1
# song_id = '880458'     # 2
# song_id = '102685612'    # 3
song_mid = '001NAENF0Tp0Ff'  # 1
# song_mid = '0001bBOZ3vF8GJ'  # 2
# song_mid = '001iIChy21ITLl'    # 3
headers_lyric = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'pgv_pvid=2559814726; ts_uid=7885404159; pgv_pvi=2160503808; RK=R5zBWDrkWH; ptcz=b3f29532b80aaa455e72b7f180ac96bbe71e809c09d01dcb702b9cfa70e27067; tvfe_boss_uuid=b79caeac19aada9c; eas_sid=K1q5n2G1T820c9u6J2k1T1g4t7; ptui_loginuin=879547165; pac_uid=1_879547165; ts_refer=www.baidu.com/link; pt2gguin=o1458140043; yq_index=10; o_cookie=1458140043; pgv_si=s1232331776; pgv_info=ssid=s2029762395; yqq_stat=0; ts_last=y.qq.com/n/yqq/album/002gnOZC4T8gXF.html',
    'referer': 'https://y.qq.com/n/yqq/song/{}.html'.format(song_mid),
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
lyric_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid={}&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(song_id)
jsonp1 = requests.get(url=lyric_url, headers=headers_lyric).content.decode('utf-8')
c = re.compile(r'jsonp1\((.*)\)')
jsons = c.findall(jsonp1)[0]
# print(jsons)
jsons = json.loads(jsons)

for data in jsons:
    print(jsons[data])
# # print(jsons)
# # 歌词内容清洗
# if 'lyric' in jsons:
#     h = re.compile(r'&#\d.;', re.S)  # 第一次
#     v = h.sub(r'', jsons['lyric'])
#     hh = re.compile(r'[\d+]', re.S)  # 第二次
#     vv = hh.sub(r'\n', v).replace('\n\n', '').replace('[]', ',').replace('\n', ',').replace(',,', ',')
#     ly = re.compile(r'\[.*\]')  # 第三次
#     lyric = ly.sub(r'', vv)
#     lyric = lyric.strip(',')
#     # lyric = json.dumps(lyric)
#     lyric = json.loads(lyric)
#     for data in lyric:
#         print(data)
#     # print(lyric,type(lyric))

