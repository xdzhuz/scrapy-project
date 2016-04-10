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

class HexungubaPipeline(object):
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
        conn.execute("select * from baselink_hexun_guba where uuid = %s", (linkmd5id, ))
        result = conn.fetchone()
        if result:
            conn.execute("""
                update baselink_hexun_guba set reply=%s, click=%s where uuid=%s
                """, (item['reply'], item['click'], linkmd5id, ))
        else:
            conn.execute("""
                insert into baselink_hexun_guba(uuid,title,article_url,author,author_url,bar_name,reply,click) 
                values(%s, %s, %s, %s, %s, %s, %s, %s)
                """, (linkmd5id, item['title'], item['article_url'], item['author'], item['author_url'],item['bar_name'], item['reply'], item['click'],))
        
    def _get_linkmd5id(self, item):
        return md5(item['article_url']).hexdigest()