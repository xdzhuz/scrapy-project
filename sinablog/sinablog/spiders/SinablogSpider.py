import scrapy
from sinablog.items import SinablogItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re
import datetime

class SinablogSpider(CrawlSpider):
    name = 'sinablog'
    allowed_domains = ['blog.sina.com.cn']
    start_urls = []
    with open(r'D:\craw\sinaid.txt') as f:
        for line in f:
                start_urls.append("http://blog.sina.com.cn/s/articlelist_"+str(int(line)) +"_0_1.html")
    
    rules = (Rule(LinkExtractor(allow=('http://blog.sina.com.cn/s/articlelist_\d+_0_\d+\.html', )), callback='parse_item',follow=True),)

    def parse_item(self, response):
        patt = re.compile(r"\d+")
        authorid = patt.findall(response.url)[0]
        items = []
        bsObj = BeautifulSoup(response.body,"lxml")
        s = bsObj.findAll("div",{"class":"articleCell SG_j_linedot1"})
        for i in s:
            item = SinablogItem()
            item['title'] = i.find("span",{"class":"atc_title"}).get_text()
            item['url'] = i.find("span",{"class":"atc_title"}).a["href"]
            time = i.find("span",{"class":"atc_tm SG_txtc"}).get_text()
            item['date'] = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M").date()
            item['authorid'] = authorid
            items.append(item)
        return items
        