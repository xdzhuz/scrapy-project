# -*- coding:utf-8 -*-
import scrapy
from sinablogcontent.items import SinablogcontentItem
from bs4 import BeautifulSoup
import re
import datetime
from urllib2 import urlopen
import MySQLdb

class SinablogcontentSpider(scrapy.Spider):
    name = "sinablogcontent"
    conn = MySQLdb.connect(host="rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com",user="licj",passwd="AAaa1234",db="middle_zixun",charset="utf8")
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT url from sinablog;""")
    start_urls = [s[0] for s in cursor.fetchall()]
    
    def parse(self, response):
        item = SinablogcontentItem()
        bsObj = BeautifulSoup(response.body,"lxml")
        item['url'] = response.url
        item['title'] = bsObj.find('h2',{"class":"titName SG_txta"}).get_text()
        item['content'] = bsObj.find('div',{"class":"articalContent"}).get_text()
        time = bsObj.find('span',{"class":"time SG_txtc"}).get_text()
        item['date'] = datetime.datetime.strptime(time, "(%Y-%m-%d %H:%M:%S)").date()
        return item
        