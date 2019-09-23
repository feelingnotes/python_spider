import requests
from lxml import etree
from bs4 import BeautifulSoup
import csv
import time
import json
import xlwt

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

url_path = 'https://www.pexels.com/search/'
word = input('请输入你想要下载的图片：（英文）')
url = url_path + word + '/'
wb_data = requests.get(url, headers = headers)
soup = BeautifulSoup(wb_data.text, 'lxml')
imgs = soup.select('article > a > img')
list = []
for img in imgs:
    photo = img.get('src')
    list.append(photo)

path = 'D://北大/python/Data/photos/'

for item in list:
    data = requests.get(item, headers=headers)
    fp = open(path+item.split('?')[0][-10:], 'wb')
    fp.write(data.content)
    fp.close()