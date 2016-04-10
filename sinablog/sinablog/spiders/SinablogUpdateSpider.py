import scrapy
from sinablog.items import SinablogItem
from bs4 import BeautifulSoup
import re
import datetime

class SinablogUpdateSpider(scrapy.Spider):
    name = 'sinablogupdate'
    allowed_domains = ['blog.sina.com.cn']
    start_urls = []
    with open(r'D:\craw\sinaid.txt') as f:
        for line in f:
                start_urls.append("http://blog.sina.com.cn/s/articlelist_"+str(int(line)) +"_0_1.html")

    def parse(self, response):
        last_time = datetime.date(2016,4,04)
        min_date = datetime.date.today()
        patt = re.compile(r"\d+")
        authorid = patt.findall(response.url)[0]
        page = patt.findall(response.url)[3]
        bsObj = BeautifulSoup(response.body,"lxml")
        s = bsObj.findAll("div",{"class":"articleCell SG_j_linedot1"})
        for i in s:
            item = SinablogItem()
            item['title'] = i.find("span",{"class":"atc_title"}).get_text()
            item['url'] = i.find("span",{"class":"atc_title"}).a["href"]
            time = i.find("span",{"class":"atc_tm SG_txtc"}).get_text()
            d = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M").date()
            if min_date>d:
                min_date = d
            item['date'] = d
            item['authorid'] = authorid
            yield item
        if min_date>last_time:
            url = "http://blog.sina.com.cn/s/articlelist_"+str(authorid) +"_0_"+str(page+1)+".html"
            yield scrapy.Request(url, callback=self.parse)
        