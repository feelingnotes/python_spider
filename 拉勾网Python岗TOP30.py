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
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer':'https://www.lagou.com/jobs/list_Python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
}

url_start = 'https://www.lagou.com/jobs/list_Python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='mydb', port=3306)
cursor = conn.cursor()

def get_page(url, params):
    s = requests.session()
    s.get(url_start, headers=headers, timeout=3)
    cookie = s.cookies
    response = s.post(url, data=params, headers=headers, cookies=cookie, timeout=3)
    json_data = json.loads(response.text)
    count = json_data['content']['positionResult']['totalCount']
    page_size = json_data['content']['positionResult']['resultSize']
    page_number = int(count/page_size) if int(count/page_size) < 30 else 30
    get_info(url, page_number, cookie)

def get_info(url, page_number, cookie):
    for page in range(1, page_number + 1):
        params = {
            'first': 'true',
            'pn': str(page),
            'kd': 'Python'
        }
        try:
            html = requests.post(url, data=params, headers=headers, cookies=cookie)
            json_data = json.loads(html.text)
            jobs = json_data['content']['positionResult']['result']
            for job in jobs:
                infos = {
                    'positionName':job['positionName'],
                    'city':job['city']
                }
                print(infos)
                time.sleep(2)
        except Exception:
            pass


if __name__== '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    params = {
        'first': 'true',
        'pn': '1',
        'kd': 'Python'
    }
    get_page(url, params)
