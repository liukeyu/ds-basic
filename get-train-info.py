"""get train info"""
#coding=utf-8


import requests
from  bs4 import BeautifulSoup
import json


BASE_URL="http://qq.ip138.com"
BSLIB = 'html5lib'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS = {'user-agent':UA}

def get_city(province,url):
	print("Begin handle:"+province)
	R=requests.get(url)
	text=R.text.encode('ISO-8859-1').decode('gbk')
	S=BeautifulSoup(text,BSLIB)
	return {city.text:get_train_info (city.text,BASE_URL+city.get("href")) for city in S.select("div > table > tbody > tr > td > a")}
		

def get_train_info(city,url):
	R=requests.get(url)
	text=R.text.encode('ISO-8859-1').decode('gbk')
	S=BeautifulSoup(text,BSLIB)
	info_list=[]
	for train_info in S.select("div#checilist > table > tbody > tr > td > a > b"):
		info_list.append(train_info.text)
	return info_list


if __name__ == '__main__':
	R=requests.get(BASE_URL+"/train/")
	text=R.text.encode('ISO-8859-1').decode('gbk')
	S=BeautifulSoup(text,BSLIB)
	all_list={item.text:get_city (item.text,BASE_URL+item.get("href")) for item in S.select("table")[4].select("tbody > tr > td > a")}
	with open("tran_info.json","w+",encoding="utf-8") as file:
		json.dump(all_list,file,ensure_ascii=False)
