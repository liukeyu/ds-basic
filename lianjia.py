import requests
import time
import json
from bs4 import BeautifulSoup
import re
import csv

BS_LIB = 'html5lib'
BASE_URL = 'http://sh.lianjia.com'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS = {'user-agent': UA}

def get_proxies():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=国内')
    ip_ports = json.loads(r.text)

    ip = ip_ports[0][0]
    port = ip_ports[0][1]


    # proxies ={'http': ('http://%s:%s' % (ip_port[0], ip_port[1])) for ip_port in ip_ports }

    proxies = {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'http://%s:%s' % (ip, port)
    }

    return  proxies


def get_apartment_info(url):
    proxies =get_proxies()
    r = requests.get(url, headers=HEADERS,proxies=proxies)
    s = BeautifulSoup(r.text, BS_LIB)
    apartments = s.select('#house-lst > li')
    with open("lj.csv","a+",newline='') as  file:
        csvwriter=csv.writer(file)
        for apm in apartments:
            price = apm.select('div.info-panel > div.col-3 > div.price > span')[0].text.strip()
            apm_section = apm.select('div.info-panel > div.col-1 > div.where > a > span')[0].text.strip()
            apm_type = apm.select('div.info-panel > div.col-1 > div.where > span')[0].text.strip()
            apm_size = apm.select('div.info-panel > div.col-1 > div.where > span')[1].text.strip()
            district = apm.select('div.info-panel > div.col-1 > div.other > div > a')[0].text.strip()
            district2 = apm.select('div.info-panel > div.col-1 > div.other > div > a')[1].text.strip()
            url = BASE_URL+apm.select('div.info-panel > h2 > a')[0].get('href')
            story = apm.select('div.info-panel > div.col-1 > div.other > div ')[0].text.strip().split('|')[1]
            story=re.sub('\s+', '', story)
            csvwriter.writerow([district,district2,apm_section,apm_type,apm_size,story,price,url])


    next_page = BASE_URL+s.select('body > div.wrapper > div.page-box.house-lst-page-box > a')[-1].get('href')

    return next_page if next_page != url else None

if __name__ == '__main__':
    NEXT_PAGE = BASE_URL+"/zufang/xuhui/a2d1l2"
    pages = 0
    while NEXT_PAGE:
        NEXT_PAGE = get_apartment_info(NEXT_PAGE)
        pages += 1
        # time.sleep(1)
        if pages == 50:
            break