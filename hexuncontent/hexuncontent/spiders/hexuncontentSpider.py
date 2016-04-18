# -*- coding:utf-8 -*-
import scrapy
from hexuncontent.items import HexuncontentItem
from bs4 import BeautifulSoup
import re
from datetime import date
from urllib2 import urlopen
import MySQLdb

class HexuncontentSpider(scrapy.Spider):
    name = "hexuncontent"
    conn = MySQLdb.connect(host="rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com",user="licj",passwd="AAaa1234",db="middle_zixun",charset="utf8")
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT article_url from baselink_hexun_guba;""")
    start_urls = [s[0] for s in cursor.fetchall()]
    
    def parse(self, response):
        item = HexuncontentItem()
        bsObj = BeautifulSoup(response.body,"lxml")
        item['url'] = response.url
        item['title'] = bsObj.find('div',{"class":"articleTitle"}).get_text()
        item['content'] = bsObj.find('div',{"class":"detail_cnt"}).get_text()
        time = bsObj.find('div',{"class":"articleInfo"}).span.get_text()
        item['date'] = self.tran_date(time)
        return item
        
    def tran_date(self, content):
        month = u'(\d)*月(\d)*日'.encode("utf-8")
        year = u'(\d)*年(\d)*月(\d)*日'.encode("utf-8")
        num = u'\d+'.encode("utf-8")
        p = re.compile(num)
        if re.match(year, content)!=None:
            numbers = p.findall(content)
            return date(int(numbers[0]), int(numbers[1]), int(numbers[2]))
        elif re.match(month, content)!=None:
            numbers = p.findall(content)
            return date(2016, int(numbers[0]), int(numbers[1]))
        else:
            return date.today()