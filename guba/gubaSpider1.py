# -*- coding:utf-8 -*-
import scrapy
from guba.items import GubaItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re
from datetime import date
from urllib2 import urlopen

class GubaSpider(CrawlSpider):
    name = "guba"
    allowed_domains = ["guba.sina.com.cn"]
    start_urls = ["http://guba.sina.com.cn/?s=bar&name=sh000001&type=0&page=1"]
    rules = (
        # Extract links matching and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('(/\?s=bar&name=sh000001&type=0&page=)(\d)*', )), callback='parse_item',follow=True),)

    def parse_item(self, response):
        items = []
        item = GubaItem()
        bsObj = BeautifulSoup(response.body,"lxml")
        s = bsObj.find("div",{"class","table_content"})
        t = bsObj.title.get_text()
        h = s.findAll("td")
        for i in range(len(h)/5):
            item["click"] = h[5*i].get_text()
            item["reply"] = h[5*i+1].get_text()
            item["title"] = h[5*i+2].get_text()
            item["url"] = "http://guba.sina.com.cn/"+h[5*i+2].a["href"]
            item["author"] = h[5*i+3].get_text()
            if h[5*i+3].findAll("i")!=[]:
                item["is_bigv"] = True
            else:
                item["is_bigv"] = False
            item["time"] = self.get_date(item["url"])
            item["type"] = t
            items.append(item)
        return items
    
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

    def get_date(self,url):
        html = urlopen(url).read()
        bsObj = BeautifulSoup(html,"lxml")
        s = bsObj.find("div",{"class":"fl_left iltp_time"})
        if s!=None:
            content = s.get_text().split()[0]
            return self.tran_date(content.encode("utf-8"))
        else:
            return self.tran_date("")