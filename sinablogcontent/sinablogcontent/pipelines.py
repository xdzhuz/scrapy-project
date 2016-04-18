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

class SinablogcontentPipeline(object):
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
        conn.execute("select * from article_content where uuid = %s", (linkmd5id, ))
        result = conn.fetchone()
        if not result:
            try:
                conn.execute("""
                    insert into article_content(uuid,title,url,content,resource, published_time) 
                    values(%s, %s, %s, %s, %s, %s)
                    """, (linkmd5id, item['title'], item['url'], item['content'], '新浪博客',item['date'],))
            except:
                pass
        
    def _get_linkmd5id(self, item):
        return md5(item['url']).hexdigest()