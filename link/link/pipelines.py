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

class JsonWithEncodingLinkedinPipeline(object):
    def __init__(self):
        self.file = codecs.open('linkedin.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreLinkedinPipeline(object):
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
        linkmd5id = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from linkedinfo where linkmd5id = %s
        """, (linkmd5id, ))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update linkedinfo set url = %s, name = %s, description = %s, location = %s, similar = %s, profile_img_s = %s, profile_img_m = %s, skills = %s
            	, skills_2 = %s, job_0 = %s, job_1 = %s, job_2 = %s, job_3 = %s, job_4 = %s, education_sum = %s, education_tot = %s, full_content = %s
            	, personal = %s, updated = %s where linkmd5id = %s
            """, (item['url'], item['name'], item['description'], item['location'], item['similar'], item['profile_img_s'],  item['profile_img_m'], item['skills']\
                , item['skills_2'], item['job_0'], item['job_1'], item['job_2'], item['job_3'], item['job_4'], item['education_sum'], item['education_tot']\
            	, item['full_content'], item['personal'], now, linkmd5id))

        else:
            conn.execute("""
                insert into linkedinfo(linkmd5id, url, name, description, location, similar, profile_img_s, profile_img_m, skills, skills_2, job_0, job_1
                , job_2, job_3, job_4, education_sum, education_tot, full_content, personal, updated) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['url'], item['name'], item['description'], item['location'], item['similar'], item['profile_img_s'],  item['profile_img_m'], item['skills']\
                , item['skills_2'], item['job_0'], item['job_1'], item['job_2'], item['job_3'], item['job_4'], item['education_sum'], item['education_tot']\
            	, item['full_content'], item['personal'], now))

    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['url']).hexdigest()

        
        
