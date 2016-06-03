# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request 
from scrapy.exceptions import DropItem  
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class MyImagesPipeline(ImagesPipeline):
    DIR_PATH='E:/Test/src/demo/static/full/%s'
    def file_path(self, request, response=None, info=None):
        global DIR_PATH
        image_guid = request.url.split('/')[-1]  
        return 'E:/Test/src/demo/static/pic/%s' % (image_guid)  
  
    '''def get_media_requests(self, item, info):
        print "12345678"
        print item['image_urls']
        print "87654321"
        for image_url in item['image_urls']:  
            yield Request(image_url)
  
    def item_completed(self, results, item, info):  
        image_paths = [x['path'] for ok, x in results if ok]  
        if not image_paths:  
            raise DropItem("Item contains no images")  
        return item'''

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
        print "pipeline"
        try:
            item['url']
            print "person"
            d = self.dbpool.runInteraction(self._do_upinsert1, item)
            return item
        except:
            try:
                item['company_url']
                print "company"
                d = self.dbpool.runInteraction(self._do_upinsert2, item)
                return item
            except:
                try:
                    item['school_url']
                    print "school"
                    d = self.dbpool.runInteraction(self._do_upinsert3, item)
                    return item
                except:
                    pass
                
    #将每行更新或写入数据库中
    def _do_upinsert1(self, conn, item):
        linkmd5id = self._get_linkmd5id1(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from linkedinfo where linkmd5id = %s
        """, (linkmd5id, ))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update linkedinfo set url = %s, name = %s, description = %s, location = %s, similar = %s, profile_img_s = %s, worked = %s, education_background = %s, industry = %s
                , skills = %s, skills_2 = %s, current_job = %s, job_0 = %s, job_1 = %s, job_2 = %s, job_3 = %s, job_4 = %s, education_sum = %s, education_tot = %s, full_content = %s
                , award = %s, updated = %s where linkmd5id = %s
            """, (item['url'], item['name'], item['description'], item['location'], item['similar'], item['profile_img_s'], item['worked'], item['education_background'], item['industry']\
                , item['skills'], item['skills_2'], item['current_job'], item['job_0'], item['job_1'], item['job_2'], item['job_3'], item['job_4'], item['education_sum'], item['education_tot']\
                , item['full_content'], item['award'], now, linkmd5id))

        else:
            conn.execute("""
                insert into linkedinfo(linkmd5id, url, name, description, location, similar, profile_img_s, worked, education_background, industry, skills, skills_2, current_job, job_0, job_1
                , job_2, job_3, job_4, education_sum, education_tot, full_content, award, field, updated) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['url'], item['name'], item['description'], item['location'], item['similar'], item['profile_img_s'], item['worked'], item['education_background']\
                , item['industry'], item['skills'], item['skills_2'], item['current_job'], item['job_0'], item['job_1'], item['job_2'], item['job_3'], item['job_4'], item['education_sum']\
                , item['education_tot'], item['full_content'], item['award'], item['field'], now))
            
        '''conn.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", item['key'])'''


    def _do_upinsert2(self, conn, item):
        idcompanyinfo = self._get_linkmd5id2(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from companyinfo where idcompanyinfo = %s
        """, (idcompanyinfo, ))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update companyinfo set company_url = %s, company_name = %s, company_logo = %s, company_img = %s, company_scale = %s, introducation = %s
                , specialties = %s, company_field = %s, website = %s, company_style = %s, location = %s, start_year = %s, updated = %s where idcompanyinfo = %s
            """, (item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_scale'], item['introducation']
                , item['specialties'], item['company_field'], item['website'], item['company_style'], item['location'], item['start_year'], now, idcompanyinfo))

        else:
            conn.execute("""
                insert into companyinfo(idcompanyinfo, company_url, company_name, company_logo, company_img, company_scale, introducation, specialties
                , company_field, website, company_style, location, start_year, field, updated)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idcompanyinfo, item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_scale'], item['introducation']
                , item['specialties'], item['company_field'], item['website'], item['company_style'], item['location'], item['start_year'], item['field'], now))
            
        '''conn.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", item['key'])'''

    def _do_upinsert3(self, conn, item):
        idschoolinfo = self._get_linkmd5id3(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from schoolinfo where idschoolinfo = %s
        """, (idschoolinfo))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update schoolinfo set school_name = %s,school_url = %s,school_logo=%s,school_img=%s,work_direction=%s,work_field=%s,gen_message=%s,website=%s,
                contact_number=%s,address=%s,school_year=%s,school_type=%s,ts_statistic=%s,finance_infor=%s,location=%s,updated=%s where idschoolinfo = %s
            """, (item['school_name'], item['school_url'],item['school_logo'],item['school_img'],item['work_direction'],item['work_field'],item['gen_message'],\
                  item['website'],item['contact_number'],item['address'],item['school_year'],item['school_type'],item['ts_statistic'],item['finance_infor'],\
                  item['location'],now,idschoolinfo))

        else:
            conn.execute("""
                insert into schoolinfo(idschoolinfo, school_name,school_url,school_logo,school_img,work_direction,work_field,gen_message,website,
                contact_number,address,school_year,school_type,ts_statistic,finance_infor,location,updated) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idschoolinfo, item['school_name'],item['school_url'],item['school_logo'],item['school_img'],item['work_direction'],item['work_field'],item['gen_message'],\
                  item['website'],item['contact_number'],item['address'],item['school_year'],item['school_type'],item['ts_statistic'],item['finance_infor'],\
                  item['location'],now))
            
        '''conn.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", item['key'])'''


    #获取url的md5编码
    def _get_linkmd5id1(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['url']).hexdigest()
    def _get_linkmd5id2(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['company_url']).hexdigest()
    def _get_linkmd5id3(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['school_url']).hexdigest()
'''
class MySQLStoreLinkedinPipeline1(object):
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
        idcompanyinfo = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from companyinfo where idcompanyinfo = %s
        """, (idcompanyinfo, ))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update companyinfo set company_url = %s, company_name = %s, company_logo = %s, company_img = %s, company_scale = %s, introducation = %s
                , specialties = %s, company_field = %s, website = %s, company_style = %s, location = %s, start_year = %s, updated = %s where idcompanyinfo = %s
            """, (item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_scale'], item['introducation']
                , item['specialties'], item['company_field'], item['website'], item['company_style'], item['location'], item['start_year'], now, idcompanyinfo))

        else:
            conn.execute("""
                insert into companyinfo(idcompanyinfo, company_url, company_name, company_logo, company_img, company_scale, introducation, specialties
                , company_field, website, company_style, location, start_year, updated)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idcompanyinfo, item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_scale'], item['introducation']
                , item['specialties'], item['company_field'], item['website'], item['company_style'], item['location'], item['start_year'], now))
            
        #conn.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", item['key'])

    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['company_url']).hexdigest()       
'''        
