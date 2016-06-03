# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class JsonWithEncodingLkischoolPipeline(object):
    def __init__(self):
        self.file = codecs.open('lkischool.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreLkischoolPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'linkedindb',
            user = 'root',
            passwd = 'bupt123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item)
        return item
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item):
        idschoolinfo = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from schoolinfo where idschoolinfo = %s
        """, (idschoolinfo))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update schoolinfo set school_name = %s,school_url = %s,school_logo=%s,school_img=%s,work_direction=%s,work_field=%s,gen_message=%s,website=%s,
                contact_number=%s,address=%s,school_year=%s,school_type=%s,ts_statistic=%s,finance_infor=%s,location=%s where idschoolinfo = %s
            """, (item['school_name'], item['school_url'],item['school_logo'],item['school_img'],item['work_direction'],item['work_field'],item['gen_message'],\
                  item['website'],item['contact_number'],item['address'],item['school_year'],item['school_type'],item['ts_statistic'],item['finance_infor'],\
                  item['location'],idschoolinfo))

        else:
            conn.execute("""
                insert into schoolinfo(idschoolinfo, school_name,school_url,school_logo,school_img,work_direction,work_field,gen_message,website,
                contact_number,address,school_year,school_type,ts_statistic,finance_infor,location) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idschoolinfo, item['school_name'],item['school_url'],item['school_logo'],item['school_img'],item['work_direction'],item['work_field'],item['gen_message'],\
                  item['website'],item['contact_number'],item['address'],item['school_year'],item['school_type'],item['ts_statistic'],item['finance_infor'],\
                  item['location']))
            
        #conn.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", item['key'])
        #conn.execute("""update taskstate set state1 = 1 where exists(select state from searchinfo where state = 0)""")
        #conn.execute("""update taskstate set state1 = 0 where not exists(select state from searchinfo where state = 0)""")

    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['school_url']).hexdigest()

        
        
