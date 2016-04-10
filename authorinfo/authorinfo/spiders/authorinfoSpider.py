# -*- coding:utf-8 -*-
import scrapy
from authorinfo.items import AuthorinfoItem
from bs4 import BeautifulSoup
import re
from datetime import date
from urllib2 import urlopen
import MySQLdb

class GubaauthorSpider(scrapy.Spider):
    name = "authorinfo"
    allowed_domains = ["guba.sina.com.cn"]
    conn = MySQLdb.connect(host="rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com",user="licj",passwd="AAaa1234",db="middle_zixun",charset="utf8")
    cursor = conn.cursor()
    cursor.execute("""SELECT weiboid FROM (
            SELECT DISTINCT baselink_sina_guba.weiboid as weiboid from baselink_sina_guba
            UNION ALL 
            SELECT DISTINCT guba_author.weiboid as weiboid from guba_author)TEMP 
            GROUP BY weiboid
            HAVING COUNT(weiboid)=1;""")
    base_url = "http://guba.sina.com.cn/u/"
    start_urls = [base_url+str(s[0]) for s in cursor.fetchall()]
    
    def parse(self, response):
        item = AuthorinfoItem()
        bsObj = BeautifulSoup(response.body,"lxml")
        s1 = bsObj.find("div",{"class":"info_num_p inp_02"})
        item['followers'] = s1.a.span.get_text()
        s2 = bsObj.find("div",{"class":"info_num_p no_border_right  inp_03"})
        item['count'] = s2.a.span.get_text()
        s3 = bsObj.find("span",{"class":"fl_left rq_span"})
        item['pop'] = s3.get_text().split(":")[1]
        mode = re.compile(r'\d+')
        item['weiboid'] = mode.findall(response.url)[0]
        s4 = bsObj.find("div",{"class":"bdi_name clearfix"})
        item['name'] = s4.div.a.get_text()
        return item