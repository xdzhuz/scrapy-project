import scrapy
from hexunguba.items import HexungubaItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re

class HexungubaSpider(CrawlSpider):
    name = 'hexunguba'
    allowed_domains = ['guba.hexun.com']
    start_urls = []
    with open(r'D:\craw\hexun.txt') as f:
        for line in f:
                start_urls.append(line[:-1])
    
    rules = (Rule(LinkExtractor(allow=('http://guba\.hexun\.com/(|t/)\d+,guba(|,p\d+)\.html', )), callback='parse_item',follow=True),)

    def parse_item(self, response):        
        items = []
        bsObj = BeautifulSoup(response.body,"lxml")
        bar_name = bsObj.title.get_text()
        s = bsObj.findAll("dl")
        for num in range(1,len(s)-3):
            i = s[num]
            item = HexungubaItem()
            item['bar_name'] = bar_name
            cs = i.dd.get_text().split("/")
            item['reply'] = cs[0]
            item['click'] = cs[1]
            h = i.findAll("a")
            item['title'] = h[0].get_text()
            item['article_url'] = h[0]["href"]
            ha = i.find("dd",{"class":"author"})
            if ha.a:
                item['author'] = ha.a.get_text()
                item['author_url'] = ha.a["href"]
            else:
                item['author'] = ha.span.get_text()
                item['author_url'] = None
            items.append(item)
        return items
        