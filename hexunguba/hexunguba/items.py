# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HexungubaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    bar_name = scrapy.Field()
    article_url = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    reply = scrapy.Field()
    click = scrapy.Field()
