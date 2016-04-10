# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    click = scrapy.Field()
    title = scrapy.Field()
    reply = scrapy.Field()
    url = scrapy.Field()
    # time = scrapy.Field()
    weiboid = scrapy.Field()
    is_bigv = scrapy.Field()
    type = scrapy.Field()
