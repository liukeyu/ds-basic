import requests
import time
from bs4 import BeautifulSoup

BS_LIB = 'html5lib'
BASE_URL = 'http://sh.lianjia.com/zufang/xuhui/a2d1l2'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS = {'user-agent': UA}


def get_apartment_info(url):
    r = requests.get(url, headers=HEADERS)
    s = BeautifulSoup(r.text, BS_LIB)
    apartments = s.select('#house-lst > li')
    for apm in apartments:
        price = apm.select('div.info-panel > div.col-3 > div.price > span')[0].text.strip()
        apm_section = apm.select('div.info-panel > div.col-1 > div.where > a > span')[0].text.strip()
        apm_type = apm.select('div.info-panel > div.col-1 > div.where > span')[0].text.strip()
        apm_size = apm.select('div.info-panel > div.col-1 > div.where > span')[1].text.strip()
        district = apm.select('div.info-panel > div.col-1 > div.other > div > a')[0].text.strip()
        district2 = apm.select('div.info-panel > div.col-1 > div.other > div > a')[1].text.strip()
        # story = apm.select('div.info-panel > div.col-1 > div.other > div ').text.strip().split('|')[1]


    next_page = s.select('body > div.wrapper > div.page-box.house-lst-page-box > a').get('href')

    return next_page if next_page != url else None

if __name__ == '__main__':
    NEXT_PAGE = BASE_URL
    pages = 0
    while NEXT_PAGE:
        NEXT_PAGE = get_apartment_info(NEXT_PAGE)
        pages += 1
        time.sleep(8)
        if pages == 23:
            break