import requests
from lxml import etree
from bs4 import BeautifulSoup
import pymysql
import time
import traceback
from multiprocessing import Pool
import re
import json
import xlwt

headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='mydb', port=3306)
cursor = conn.cursor()

def get_article_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    try:
        infos = selector.xpath('//ul[@class="note-list"]/li')

        for info in infos:
            try:
                author = info.xpath('div/div/a/text()')[0]
                title = info.xpath('div/a/text()')[0].strip()
                content = info.xpath('div/p/text()')[0].strip()
                commtent = info.xpath('div/div/a[2]/text()')[1].strip()
                if len(info.xpath('div/div/span[2]/text()')) != 0:
                    thumbs = info.xpath('div/div/span[2]/text()')[0].strip()
                else:
                    thumbs = '0'
                rewards = info.xpath('div/div/span[3]/text()')
                if len(rewards) == 0:
                    rewards = '无'
                else:
                    rewards = rewards[0].strip()
                # print(title, content, commtent, thumbs,rewards)
                cursor.execute("insert into jianshuarticle (author, title, content, rewards, comment, thumbs) values (%s,%s,%s,%s,%s,%s)", (str(author), str(title), str(content), str(rewards), str(commtent), str(thumbs)))
                conn.commit()
            except Exception:
                traceback.print_exc()
                pass
    except Exception:
        traceback.print_exc()
        return ""

if __name__== '__main__':
    urls = ['https://www.jianshu.com/c/bDHhpK?order_by=added_at&page={}'.format(number) for number in range(1, 50)]
    pool = Pool(processes=4)
    pool.map(get_article_info, urls)
