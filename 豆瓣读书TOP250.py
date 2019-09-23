# -*- coding:utf-8 -*-
import requests
from lxml import etree
import csv
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def get_links(url):
    wb_data = requests.get(url, headers=headers)
    selector = etree.HTML(wb_data.text)
    infos = selector.xpath('//li[@class="subject-item"]')
    for info in infos:
        name = info.xpath('div[2]/h2/a/@title')[0]
        url = info.xpath('div[2]/h2/a/@href')[0]
        book_infos = info.xpath('div[2]/div[1]/text()')[0]
        author = book_infos.split('/')[0].strip()
        publisher = book_infos.split('/')[-3].strip()
        date = book_infos.split('/')[-2].strip()
        price = book_infos.split('/')[-1].strip()
        rate = info.xpath('div[2]/div[2]/span[2]/text()')[0] if len(info.xpath('div[2]/div[2]/span[2]/text()')) != 0 else '空'
        # print((name, url, author, publisher, date, price, rate))
        writer.writerow((name, url, author, publisher, date, price, rate))

if __name__ == '__main__':
    urls = [
        'https://book.douban.com/tag/%E5%88%9B%E4%B8%9A?start={}&type=T'.format(number)
        for number in range(0, 250, 20)
    ]
    fp = open('D://北大/python/Data/豆瓣.csv', 'w+', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('name', 'url', 'author', 'publisher', 'date', 'price', 'rate'))
    for url in urls:
        get_links(url)
        time.sleep(2)
    fp.close()
