# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.exceptions import CloseSpider
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from crawler.getuser import free_user_in_mysql

class MyImagesPipeline(ImagesPipeline):
    DIR_PATH='E:/Test/src/demo/static/full/%s'
    def file_path(self, request, response=None, info=None):
        global DIR_PATH
        image_guid = request.url.split('/')[-1]
        return 'E:/Test/src/demo/static/pic/%s' % (image_guid)


class JsonWithEncodingLinkedinPipeline(object):
    def process_item(self, item, spider):
        try:
            item['profile_url']
            file = codecs.open('profile.json', 'a', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            file.write(line)
            return item
        except:
            try:
                item['company_url']
                file = codecs.open('company.json', 'a', encoding='utf-8')
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                file.write(line)
                return item
            except:
                try:
                    item['school_url']
                    file = codecs.open('school.json', 'a', encoding='utf-8')
                    line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                    file.write(line)
                    return item
                except:
                    pass
    def spider_closed(self, spider):
        self.file.close()
        raise CloseSpider('Shutdown by ctrl-c')


class MySQLStoreLinkedinPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'linkedin',
            user = 'root',
            passwd = 'bupt123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            item['profile_url']
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
                select 1 from profileitem where idprofileitem = %s
        """, (linkmd5id,))
        ret = conn.fetchone()
        profile_current = '^'.join(item['profile_current'])
        profile_previous = '^'.join(item['profile_previous'])
        profile_education = '^'.join(item['profile_education'])
        profile_experience_bkgd = '^'.join(item['profile_experience_bkgd'])
        profile_honors_bkgd = '^'.join(item['profile_honors_bkgd'])
        profile_projects_bkgd = '^'.join(item['profile_projects_bkgd'])
        profile_top_skills_bkgd = '^'.join(item['profile_top_skills_bkgd'])
        profile_also_knows_bkgd = '^'.join(item['profile_also_knows_bkgd'])
        profile_education_bkgd = '^'.join(item['profile_education_bkgd'])
        profile_organizations_bkgd = '^'.join(item['profile_organizations_bkgd'])
        profile_organizations_supports = '^'.join(item['profile_organizations_supports'])
        profile_causes_cares = '^'.join(item['profile_causes_cares'])
        if ret:
            conn.execute("""
                update profileitem set profile_url = %s, profile_img = %s, profile_name = %s, profile_headline = %s, profile_location = %s, profile_industry = %s, profile_current = %s, profile_previous = %s, profile_education = %s, profile_homepage = %s, profile_summary_bkgd = %s, profile_experience_bkgd = %s, profile_honors_bkgd = %s, profile_projects_bkgd = %s, profile_top_skills_bkgd = %s, profile_also_knows_bkgd = %s, profile_education_bkgd = %s, profile_organizations_bkgd = %s, profile_organizations_supports = %s, profile_causes_cares = %s
                , updated = %s where idprofileitem = %s
            """, (item['profile_url'], item['profile_img'], item['profile_name'], item['profile_headline'], item['profile_location'], item['profile_industry'], profile_current, profile_previous, profile_education, item['profile_homepage'], item['profile_summary_bkgd'], profile_experience_bkgd, profile_honors_bkgd, profile_projects_bkgd, profile_top_skills_bkgd, profile_also_knows_bkgd, profile_education_bkgd, profile_organizations_bkgd, profile_organizations_supports, profile_causes_cares, now, linkmd5id))
        else:
            conn.execute("""
                insert into profileitem(idprofileitem, profile_url, profile_img, profile_name, profile_headline, profile_location, profile_industry, profile_current, profile_previous, profile_education, profile_homepage, profile_summary_bkgd, profile_experience_bkgd, profile_honors_bkgd, profile_projects_bkgd, profile_top_skills_bkgd, profile_also_knows_bkgd, profile_education_bkgd, profile_organizations_bkgd, profile_organizations_supports, profile_causes_cares, updated)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['profile_url'], item['profile_img'], item['profile_name'], item['profile_headline'], item['profile_location'], item['profile_industry'], profile_current, profile_previous, profile_education, item['profile_homepage'], item['profile_summary_bkgd'], profile_experience_bkgd, profile_honors_bkgd, profile_projects_bkgd, profile_top_skills_bkgd, profile_also_knows_bkgd, profile_education_bkgd, profile_organizations_bkgd, profile_organizations_supports, profile_causes_cares, now))


    def _do_upinsert2(self, conn, item):
        linkmd5id = self._get_linkmd5id2(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from companyitem where idcompanyitem = %s
        """, (linkmd5id,))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update companyitem set company_url = %s, company_name = %s, company_logo = %s, company_img = %s, company_description = %s, company_specialties = %s, company_website = %s, company_industy = %s, company_type = %s, company_headquarters = %s, company_size = %s, company_founded = %s, updated = %s where idcompanyitem = %s
            """, (item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_description'], item['company_specialties'], item['company_website'], item['company_industy'], item['company_type'], item['company_headquarters'], item['company_size'], item['company_founded'], now, linkmd5id))
        else:
            conn.execute("""
                insert into companyitem(idcompanyitem, company_url, company_name, company_logo, company_img, company_description, company_specialties, company_website, company_industy, company_type, company_headquarters, company_size, company_founded, updated)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['company_url'], item['company_name'], item['company_logo'], item['company_img'], item['company_description'], item['company_specialties'], item['company_website'], item['company_industy'], item['company_type'], item['company_headquarters'], item['company_size'], item['company_founded'], now))

    def _do_upinsert3(self, conn, item):
        linkmd5id = self._get_linkmd5id3(item)
        #print linkmd5id
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from schoolitem where idschoolitem = %s
        """, (linkmd5id,))
        ret = conn.fetchone()
        school_notables = '^'.join(item['school_notables'])
        students_live_place = '^'.join(item['students_live_place'])
        students_live_num = '^'.join(item['students_live_num'])
        students_work_company = '^'.join(item['students_work_company'])
        students_work_num = '^'.join(item['students_work_num'])
        students_do_field = '^'.join(item['students_do_field'])
        students_do_num = '^'.join(item['students_do_num'])
        students_studied_subject = '^'.join(item['students_studied_subject'])
        students_studied_num = '^'.join(item['students_studied_num'])
        students_skill_field = '^'.join(item['students_skill_field'])
        students_skill_num = '^'.join(item['students_skill_num'])
        if ret:
            conn.execute("""
                update schoolitem set school_url = %s, school_name = %s, school_logo = %s, school_img = %s, school_location = %s, genarl_information = %s, school_homepage = %s, school_email = %s, school_type = %s, contact_number = %s, school_year = %s, school_address = %s, undergrad_students = %s, graduate_students = %s, male = %s, female = %s, faculty = %s, admitted = %s, total_population = %s, graduated = %s, student_faculty_ratio = %s, tuition = %s, school_notables = %s, students_live_place = %s, students_live_num = %s, students_work_company = %s, students_work_num = %s, students_do_field = %s, students_do_num = %s, students_studied_subject = %s, students_studied_num = %s, students_skill_field = %s, students_skill_num = %s, updated = %s where idschoolitem = %s
            """, (item['school_url'], item['school_name'], item['school_logo'], item['school_img'], item['school_location'], item['genarl_information'], item['school_homepage'], item['school_email'], item['school_type'], item['contact_number'], item['school_year'], item['school_address'], item['undergrad_students'], item['graduate_students'], item['male'], item['female'], item['faculty'], item['admitted'], item['total_population'], item['graduated'], item['student_faculty_ratio'], item['tuition'], school_notables, students_live_place, students_live_num, students_work_company, students_work_num, students_do_field, students_do_num, students_studied_subject, students_studied_num, students_skill_field, students_skill_num, now, linkmd5id))
        else:
            conn.execute("""
                insert into schoolitem(idschoolitem, school_url, school_name, school_logo, school_img, school_location, genarl_information, school_homepage, school_email,
                school_type, contact_number, school_year, school_address, undergrad_students, graduate_students, male, female, faculty, admitted, total_population, graduated, student_faculty_ratio, tuition, school_notables, students_live_place, students_live_num, students_work_company, students_work_num, students_do_field, students_do_num, students_studied_subject, students_studied_num, students_skill_field, students_skill_num, updated)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['school_url'], item['school_name'], item['school_logo'], item['school_img'], item['school_location'], item['genarl_information'], item['school_homepage'], item['school_email'], item['school_type'], item['contact_number'], item['school_year'], item['school_address'], item['undergrad_students'], item['graduate_students'], item['male'], item['female'], item['faculty'], item['admitted'], item['total_population'], item['graduated'], item['student_faculty_ratio'], item['tuition'], school_notables, students_live_place, students_live_num, students_work_company, students_work_num, students_do_field, students_do_num, students_studied_subject, students_studied_num, students_skill_field, students_skill_num, now))


    #获取url的md5编码
    def _get_linkmd5id1(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['profile_url'][0:80]).hexdigest()
    def _get_linkmd5id2(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['company_url'][0:65]).hexdigest()
    def _get_linkmd5id3(self, item):
        #url进行md5处理，避免重复采集
        return md5(item['school_url'][0:75]).hexdigest()
