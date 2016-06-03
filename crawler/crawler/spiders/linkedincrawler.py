# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from crawler.items import CrawlerItem
from selenium import webdriver
from scrapy.http import Request
from crawler.configs import LinkedInAccount
import cPickle as pickle
import codecs
import os
import sys
import string
import scrapy
import MySQLdb
import re
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedincrawl"
    allowed_domains = ["www.linkedin.com"]
    account = LinkedInAccount().get()
    start_urls = ['https://www.linkedin.com/uas/login']
    def __init__(self):
        self.key = self.account['key']
        self.password = self.account['password']
        self.url_login = self.start_urls[0]
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)
        self.timeout = 5


    def start_requests(self):
        return [Request("https://www.linkedin.com/uas/login", callback = self.get_linkedin_list)]


    def get_cookie_from_linkedin(self):

        self.driver.get(self.url_login)
        self.driver.find_element_by_id("session_key-login").send_keys(self.key)
        self.driver.find_element_by_id("session_password-login").send_keys(self.password)
        bttn = self.driver.find_element_by_id("btn-primary")
        bttn.click()
        self.driver.maximize_window()
        time.sleep(5)

        cookie_list = self.driver.get_cookies()
        cookie_dict = {}
        for cookie in cookie_list:
            #写入文件
            f = open(cookie['name']+'.link','w')
            pickle.dump(cookie, f)
            f.close()

            if cookie.has_key('name') and cookie.has_key('value'):
                cookie_dict[cookie['name']] = cookie['value']

        return cookie_dict


    def get_cookie_from_cache(self):

        cookie_dict = {}
        for parent, dirnames, filenames in os.walk('./'):
            for filename in filenames:
                if filename.endswith('.link'):
                    print filename
                    with open(filename, 'r') as f:
                        d = pickle.load(f)

                        if d.has_key('name') and d.has_key('value') and d.has_key('expiry'):
                            expiry_date = int(d['expiry'])
                            if expiry_date > (int)(time.time()):
                                cookie_dict[d['name']] = d['value']
                            else:
                                return {}

        return cookie_dict


    def get_cookie(self):

        cookie_dict = self.get_cookie_from_cache()
        if not cookie_dict:
            cookie_dict = self.get_cookie_from_linkedin()

        return cookie_dict


    def get_linkedin_list(self):
        import requests
        from bs4 import BeautifulSoup as bs

        self.cookdic = self.get_cookie()
        url_list = ['http://www.linkedin.com/vsearch/p?keywords=vijay kumar&company=University of Pennsylvania']
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

        #通过数据库字段判断request的url类型 为person 还是school 还是company
        r = requests.get(url_list[0], headers=self.headers, cookies=self.cookdic, timeout=self.timeout)
        soup = BeautifulSoup(r.text, 'lxml')

        profilecards = soup.find_all(class_ = "mod result")
        for profilecard in profilecards:
            profile = profilecard.div.h3.a.get('href')
            yield scrapy.Request(profile, headers=self.headers, cookies=self.cookdic, timeout=self.timeout, callback=self.parse_person_item)


    def parse_person_item(self, response):
        if response:
            item = ProfileItem()
            sel = Selector(response)
            items = []
            #item['website'] = None
            try:
                item['profile_url'] = str(response.url)
                print item['profile_url']
            except:
                pass

            try:
                item['profile_img'] = None
                item['profile_img'] = sel.xpath('//div[@id="control_gen_3"]/img/@src').extract()
            except:
                pass

            try:
                item['profile_name'] = None
                item['profile_name'] = sel.xpath('//div[@id="name"]/h1/span/span/text()').extract()
            except:
                pass

            try:
                item['profile_headline'] = None
                item['profile_headline'] = sel.xpath('//div[@id="headline"]/p/text()').extract()
            except:
                pass

            try:
                item['profile_location'] = None
                item['profile_location'] = sel.xpath('//div[@id="location"]/dl/dd[1]/span/a/text()').extract()
            except:
                pass

            try:
                item['profile_industry'] = None
                item['profile_industry'] = sel.xpath('//div[@id="location"]/dl/dd[2]/a/text()').extract()
            except:
                pass

            try:
                item['profile_current'] = []
                currents = sel.xpath('//div[@id="overview-summary-current"]/td/ol/li')
                for current in currents:
                    ss = current.xpath('string(.)').extract()
                    item['profile_current'].append(ss)
            except:
                pass

            try:
                item['profile_previous'] = []
                previouses = sel.xpath('//div[@id="overview-summary-past"]/td/ol/li')
                for previous in previouses:
                    ss = previous.xpath('string(.)').extract()
                    item['profile_previous'].append(ss)
            except:
                pass

            try:
                item['profile_education'] = []
                educations = sel.xpath('//div[@id="overview-summary-education"]/td/ol/li')
                for education in educations:
                    ss = education.xpath('string(.)').extract()
                    item['profile_education'].append(ss)
            except:
                pass

            try:
                item['profile_education'] = []
                educations = sel.xpath('//div[@id="overview-summary-education"]/td/ol/li')
                for education in educations:
                    ss = education.xpath('string(.)').extract()
                    item['profile_education'].append(ss)
            except:
                pass

            try:
                item['profile_homepage'] = None
                item['profile_homepage'] = sel.xpath('//dl[@class="public-profile"]/dd/a/text()').extract()
            except:
                pass

            try:
                item['profile_summary_bkgd'] = None
                item['profile_summary_bkgd'] = sel.xpath('//div[@class="summary-item-view"]/div/p/text()').extract()
            except:
                pass

            try:
                item['profile_experience_bkgd'] = []
                experiences = sel.xpath('//div[@id="background-experience"]/div')
                for experience in experiences:
                    ss = experience.xpath('string(.)').extract()
                    item['profile_experience_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_honors_bkgd'] = []
                honors = sel.xpath('//div[@id="background-honors"]/div')
                for honor in honors:
                    ss = honor.xpath('string(.)').extract()
                    item['profile_honors_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_honors_bkgd'] = []
                honors = sel.xpath('//div[@id="background-honors"]/div')
                for honor in honors:
                    ss = honor.xpath('string(.)').extract()
                    item['profile_honors_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_projects_bkgd'] = []
                projects = sel.xpath('//div[@id="background-projects"]/div')
                for project in projects:
                    ss = project.xpath('string(.)').extract()
                    item['profile_projects_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_top_skills_bkgd'] = []
                skills = sel.xpath('//div[@id="profile-skills"]/ul[1]/li/span/span')
                for skill in skills:
                    ss = skill.xpath('string(.)').extract()
                    item['profile_top_skills_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_also_knows_bkgd'] = []
                knows = sel.xpath('//div[@id="profile-skills"]/ul[2]/li/div/span/span')
                for know in knows:
                    ss = know.xpath('string(.)').extract()
                    item['profile_also_knows_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_education_bkgd'] = []
                educations_bk = sel.xpath('//div[@id="background-education"]/div')
                for education_bk in educations_bk:
                    ss = education_bk.xpath('string(.)').extract()
                    item['profile_education_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_organizations_bkgd'] = []
                organizations = sel.xpath('//div[@id="background-organizations"]/div')
                for organization in organizations:
                    ss = organization.xpath('string(.)').extract()
                    item['profile_organizations_bkgd'].append(ss)
            except:
                pass

            try:
                item['profile_organizations_supports'] = []
                organizations_sup = sel.xpath('//div[@id="volunteering-organizations-view"]/div/ul/li')
                for organization_sup in organizations_sup:
                    ss = organization_sup.xpath('string(.)').extract()
                    item['profile_organizations_supports'].append(ss)
            except:
                pass

            try:
                item['profile_causes_cares'] = []
                causes = sel.xpath('//div[@id="volunteering-causes-view"]/div/ul/li')
                for cause in causes:
                    ss = cause.xpath('string(.)').extract()
                    item['profile_causes_cares'].append(ss)
            except:
                pass

            items.append(item)
        else:
            print "no response"

        return items


    def parse_school_item(self, response):
        if response:
            item = SchoolItem()
            sel = Selector(response)

            try:
                item['school_url'] = str(response.url)
                print item['school_url']
            except:
                pass

            try:
                item['school_name'] = None
                item['school_name'] = sel.xpath('//div[@class="header"]/div[1]/div/h1/text()').extract()
            except:
                pass

            try:
                item['school_location'] = None
                item['school_location'] = sel.xpath('//div[@class="header"]/div[1]/div/h4/text()').extract()
            except:
                pass

            try:
                item['school_logo'] = None
                item['school_logo'] = sel.xpath('//div[@class="header"]/a/img/@src').extract()
            except:
                pass

            try:
                item['school_img'] = None
                item['school_img'] = sel.xpath('//a[@id="cover-photo-show-treasury"]/img/@src').extract()
            except:
                pass

            try:
                item['genarl_information'] = None
                item['genarl_information'] = sel.xpath('//dd[@class="full-description"]/text()').extract()
            except:
                pass

            try:
                item['school_homepage'] = None
                item['school_homepage'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[1]/dd[1]/a/text()').extract()
            except:
                pass

            try:
                item['school_email'] = None
                item['school_email'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[2]/dd[1]/a/text()').extract()
            except:
                pass

            try:
                item['school_type'] = None
                item['school_type'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[2]/dd[2]/text()').extract()
            except:
                pass

            try:
                item['contact_number'] = None
                item['contact_number'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[1]/dd[2]/text()').extract()
            except:
                pass

            try:
                item['school_year'] = None
                item['school_year'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[2]/dd[3]/text()').extract()
            except:
                pass

            try:
                item['school_address'] = None
                item['school_address'] = sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[1]/dd[3]/text()').extract() + sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[1]/dd[4]/text()').extract() + sel.xpath('//dl[@class="school-meta-data"]/dd[2]/dl[1]/dd[5]/text()').extract()
            except:
                pass

            try:
                item['undergrad_students'] = None
                item['undergrad_students'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[1]/text()').extract()
            except:
                pass

            try:
                item['graduate_students'] = None
                item['graduate_students'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[2]/text()').extract()
            except:
                pass

            try:
                item['faculty'] = None
                item['faculty'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[3]/text()').extract()
            except:
                pass

            try:
                item['total_population'] = None
                item['total_population'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[4]/text()').extract()
            except:
                pass

            try:
                item['student/faculty_ratio'] = None
                item['student/faculty_ratio'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[5]/text()').extract()
            except:
                pass

            try:
                item['male'] = None
                item['male'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[2]/dd[1]/text()').extract()
            except:
                pass

            try:
                item['female'] = None
                item['female'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[2]/dd[2]/text()').extract()
            except:
                pass

            try:
                item['admitted'] = None
                item['admitted'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[2]/dd[3]/text()').extract()
            except:
                pass

            try:
                item['graduated'] = None
                item['graduated'] = sel.xpath('//dl[@class="school-meta-data"]/dd[3]/dl[1]/dd[1]/text()').extract()
            except:
                pass

            try:
                item['tuition'] = None
                item['tuition'] = sel.xpath('//dl[@class="school-meta-data"]/dd[4]/dl[2]/text()').extract()
            except:
                pass

            yield scrapy.Request(response.url.replace('school','notable'), headers=self.headers, cookies=self.cookdic, meta=item, timeout=self.timeout, callback=self.parse_school_notable)
        else:
            print "no response"


    def parse_school_notable(self, response):
        if response:
            item = response.meta
            sel = Selector(response)

            try:
                item['school_notables'] = []
                notables = sel.xpath('//ul[@id="my-feed-post"]/li/div/div[1]/a')
                for notable in notables:
                    ss = notable.xpath('//@href').extract()
                    item['school_notables'].append(ss)
            except:
                pass

            yield scrapy.Request(response.url.replace('notable','alumni'), headers=self.headers, cookies=self.cookdic, meta=item, timeout=self.timeout, callback=self.parse_school_notable)
        else:
            print "no response"


    def parse_school_alumni(self, response):
        if response:
            item = response.meta
            sel = Selector(response)

            items[]

            try:
                item['students_live_place'] = []
                live_places = sel.xpath('//div[@class="carousel-content"]/ul/li[1]/ul/li')
                for live_place in live_places:
                    ss = live_place.xpath('//a/div[2]/p[1]/text()').extract()
                    item['students_live_place'].append(ss)
            except:
                pass

            try:
                item['students_live_num'] = []
                live_num = sel.xpath('//div[@class="carousel-content"]/ul/li[1]/ul/li')
                for num in live_num:
                    ss = num.xpath('//a/div[2]/p[2]/text()').extract()
                    item['students_live_place'].append(ss)
            except:
                pass

            try:
                item['students_work_company'] = []
                companys= sel.xpath('//div[@class="carousel-content"]/ul/li[2]/ul/li')
                for company in companys:
                    ss = company.xpath('//a/div[2]/p[1]/text()').extract()
                    item['students_work_company'].append(ss)
            except:
                pass

            try:
                item['students_work_num'] = []
                work_num= sel.xpath('//div[@class="carousel-content"]/ul/li[2]/ul/li')
                for num in work_num:
                    ss = num.xpath('//a/div[2]/p[2]/text()').extract()
                    item['students_work_num'].append(ss)
            except:
                pass

            try:
                item['students_do_field'] = []
                do_field= sel.xpath('//div[@class="carousel-content"]/ul/li[3]/ul/li')
                for field in do_field:
                    ss = field.xpath('//a/div[2]/p[1]/text()').extract()
                    item['students_do_field'].append(ss)
            except:
                pass

            try:
                item['students_do_num'] = []
                do_num= sel.xpath('//div[@class="carousel-content"]/ul/li[3]/ul/li')
                for num in do_num:
                    ss = num.xpath('//a/div[2]/p[2]/text()').extract()
                    item['students_do_num'].append(ss)
            except:
                pass

            try:
                item['students_studied_subject'] = []
                subjects= sel.xpath('//div[@class="carousel-content"]/ul/li[4]/ul/li')
                for subject in subjects:
                    ss = subject.xpath('//a/div[2]/p[1]/text()').extract()
                    item['students_studied_subject'].append(ss)
            except:
                pass

            try:
                item['students_studied_num'] = []
                studied_num= sel.xpath('//div[@class="carousel-content"]/ul/li[4]/ul/li')
                for num in studied_num:
                    ss = num.xpath('//a/div[2]/p[2]/text()').extract()
                    item['students_studied_num'].append(ss)
            except:
                pass

            try:
                item['students_skill_field'] = []
                skills= sel.xpath('//div[@class="carousel-content"]/ul/li[5]/ul/li')
                for skill in skills:
                    ss = skill.xpath('//a/div[2]/p[1]/text()').extract()
                    item['students_skill_field'].append(ss)
            except:
                pass

            try:
                item['students_skill_num'] = []
                skill_num= sel.xpath('//div[@class="carousel-content"]/ul/li[5]/ul/li')
                for num in skill_num:
                    ss = num.xpath('//a/div[2]/p[2]/text()').extract()
                    item['students_skill_num'].append(ss)
            except:
                pass

            items.append(item)
        else:
            print "no response"
        return items
