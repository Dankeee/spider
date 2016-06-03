# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class JsonCnasPipeline(object):
    def __init__(self):
        self.file = codecs.open('cnas.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class MySQLCnasPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'cnas',
            user = 'root',
            passwd = 'bupt123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_insert, item)
        return item
    
    def _do_insert(self, conn, item):
        for n in item['register_id']:
            ss = n
        
        conn.execute("""
                select 1 from cnastable where register_id = %s
        """, (ss, ))
        ret = conn.fetchone()
        if not ret:
            conn.execute("""insert into cnastable(register_id, url, name, other_name, contacts, tel, postalcode, fax, website, email, address, effective_date)
                         values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (item['register_id'], item['url'], item['name'], item['other_name'], item['contacts']
                        , item['tel'], item['postalcode'], item['fax'], item['website'], item['email'], item['address'], item['effective_date']))
        else:
            conn.execute("""update cnastable set url=%s, name=%s, other_name=%s, contacts=%s, tel=%s, postalcode=%s, fax=%s, website=%s, email=%s, address=%s
                        , effective_date=%s where register_id=%s""", (item['url'], item['name'], item['other_name'], item['contacts'], item['tel']
                        , item['postalcode'], item['fax'], item['website'], item['email'], item['address'], item['effective_date'], item['register_id'], ))
            
