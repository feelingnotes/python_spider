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

def get_time_info(url, page):
    if url.find('page='):
        page = page + 1
        if page > 10:
            return
    html = requests.get(url, headers = headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        try:
            dd = info.xpath('div/div[1]/div/span/@data-datetime')
            title = info.xpath('div/a/text()')
            if len(title) == 0:
                continue
            print(dd, title)
            cursor.execute("insert into jianshutimeline (title, time) values (%s, %s)", (str(title), str(dd)))
            conn.commit()  #重要！！！
        except:
            traceback.print_exc()
            pass
    id_infos = selector.xpath('//ul[@class="note-list"]/li/@id')
    if len(id_infos) > 1:
        feed_id = id_infos[-1]
        id = feed_id.split('-')[1]
        next_url = 'https://www.jianshu.com/users/9104ebf5e177/timeline?max_id={}&page={}'.format(id, page)
        get_time_info(next_url, page)

if __name__== '__main__':
    url = 'https://www.jianshu.com/users/9104ebf5e177/timeline?page=1'
    get_time_info(url, 1)
