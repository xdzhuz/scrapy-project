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

class MySQLStoreGubaPipeline(object):
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
        linkmd5id = self._get_linkmd5id(item)
        conn.execute("select * from baselink_sina_guba where uuid = %s", (linkmd5id, ))
        result = conn.fetchone()
        if result and item['weiboid']!=None:
            conn.execute("update baselink_sina_guba set weiboid=%s where uuid=%s",(item['weiboid'],linkmd5id, ))
        elif item['weiboid']!=None:
            conn.execute("""
                insert into baselink_sina_guba(uuid, title, url, author, weiboid, page_view, reply_cnt,is_bigv,type) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (linkmd5id, item['title'], item['url'], item['author'], item['weiboid'],item['click'],item['reply'],item['is_bigv'],item['type']))
        elif not result:
            conn.execute("""
                insert into baselink_sina_guba(uuid, title, url, author, page_view, reply_cnt,is_bigv,type) 
                values(%s, %s, %s, %s, %s, %s, %s, %s)
                """, (linkmd5id, item['title'], item['url'], item['author'], item['click'],item['reply'],item['is_bigv'],item['type']))
        
    def _get_linkmd5id(self, item):
        return md5(item['url']).hexdigest()

class JsonWithEncodingGubaPipeline(object):
    def __init__(self):
        self.file = codecs.open('tencent.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close(
)