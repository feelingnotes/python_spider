
import requests
from lxml import etree
import csv
import time
import xlwt


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

all_info_list = []

def get_links(url):
    wb_data = requests.get(url, headers=headers)
    selector = etree.HTML(wb_data.text)
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li')
    for info in infos:
        title = info.xpath('div[2]/h4/a/text()')[0]
        href = info.xpath('div[2]/h4/a/@href')[0][2:]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style_1 = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        style_2 = info.xpath('div[2]/p[1]/a[3]/text()')[0]
        style = style_1 + '·' + style_2
        complete = info.xpath('div[2]/p[1]/span/text()')[0]
        introduce = info.xpath('div[2]/p[2]/text()')[0].strip()
        info_list = [title, href, author, style, complete, introduce]
        all_info_list.append(info_list)
        # print((title, href, author, style, complete, introduce))


if __name__ == '__main__':
    urls = [
        'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page={}'.format(number)
        for number in range(1, 100)
    ]
    for url in urls:
        get_links(url)
        time.sleep(1)
    header = ['title', 'href', 'author', 'style', 'complete', 'introduce']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    i = 1
    for list in all_info_list:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
book.save(r"D://北大/python/Data/起点中文TOP100.xls")