# -*-coding:utf-8-*-
import requests
from lxml import etree


def func(url, book_name):
    code = requests.get(url).status_code
    print(code)

    if code == 200:
        req = requests.get(url)
        htm = req.content.decode('gbk')
        html = etree.HTML(htm)

        # 内容
        content = html.xpath('//div[@id="pagecontent"]/text()')

        if content:
            title = html.xpath('//h1/text()')[0]
            content = '\n\n'.join(content)

            with open('%s.txt' % book_name, 'a+', encoding='utf8') as f:
                f.write('\n' + '\n' + title + '\n' + '\n')
                f.write(content)

            # 下一页的访问路径
            if '下一页' in htm:
                next_url = html.xpath('//div[@class="link"]/a[5]/@href')[0]
                next_url = 'http://www.ggdown.com/39/39629/' + next_url

                func(next_url, book_name)   # 递归调用

            # 结束
            else:
                pass

        else:
            pass

    else:
        pass


if __name__ == '__main__':
    # base_url = 'http://www.ggdown.com/39/39629/12518237.html'
    base_url = input('请输入访问网址:')
    name = input('请输入书名:')
    func(base_url, name)
