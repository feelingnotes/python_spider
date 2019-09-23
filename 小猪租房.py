# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def judgement_sex(class_name):
    if class_name == 'member_ico1':
        return '女'
    else:
        return '男'

def get_info(href):
    wb_data = requests.get(href, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.pho_info > h4 > em')
    addresses = soup.select('div.pho_info > p')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    for title, address, price, img, name, sex in zip(titles, addresses, prices, imgs, names, sexs):
        data = {
            'title':title.get_text().strip(),
            'address':address.get("title"),
            'price':price.get_text(),
            'img':img.get("src"),
            'name':name.get_text(),
            'sex':judgement_sex(sex.get("class"))
        }
        print json.dumps(data, encoding="UTF-8", ensure_ascii=False)

def get_links(url):
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        href = link.get("href")
        get_info(href)

if __name__ == '__main__':
    urls = [
        'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number)
        for number in range(1, 14)
    ]
    for url in urls:
        get_links(url)
        time.sleep(2)
