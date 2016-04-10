# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import codecs
from twisted.enterprise import adbapi
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
import json

class MySQLStoreAuthorinfoPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', 
                host = 'rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com', db='middle_zixun',
                user='licj', passwd='AAaa1234', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item)
        return item
    
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item):
        conn.execute("select * from guba_author where weiboid = %s", (item['weiboid'], ))
        result = conn.fetchone()
        if result:
            conn.execute("update guba_author set name=%s, followers=%s, popularity=%s, gubacount=%s where weiboid=%s",(item['name'],item['followers'],item['pop'],item['count'],item['weiboid'],))
        else:
            conn.execute("""
                insert into guba_author(weiboid, name, followers, popularity, gubacount) 
                values(%s, %s, %s, %s, %s)
                """, (item['weiboid'],item['name'],item['followers'],item['pop'],item['count'],))