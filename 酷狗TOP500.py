# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def get_links(url):
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')
    songs = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    times = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')
    for rank, song, time in zip(ranks, songs, times):
        data = {
            'rank':rank.get_text().strip(),
            'author':song.get("title").split('-')[0].strip(),
            'title':song.get("title").split('-')[1].strip(),
            'time':time.get_text().strip()
        }
        print json.dumps(data, encoding="UTF-8", ensure_ascii=False)

if __name__ == '__main__':
    urls = [
        'https://www.kugou.com/yy/rank/home/{}-8888.html'.format(number)
        for number in range(1, 23)
    ]
    for url in urls:
        get_links(url)
        time.sleep(2)
