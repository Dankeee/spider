# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from crawler.items import ProfileItem, SchoolItem, CompanyItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from scrapy.http import Request
from crawler.configs import LinkedInUserAgent,MySQLConnect
import cPickle as pickle
import codecs
import os
import sys
import string
import scrapy
import re
import time
import random
from crawler.gettask import get_task_from_mysql
from crawler.getuser import get_user_from_mysql, ban_user_from_mysql, free_user_in_mysql
reload(sys)
sys.setdefaultencoding('utf-8')

class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedincrawl"
    allowed_domains = ["www.linkedin.com"]
    account = get_user_from_mysql()
    ua = LinkedInUserAgent().get()
    # sa = LinkedInProxy().get()
    # service_args = [ '--proxy=localhost:9150', '--proxy-type=socks5', ]
    start_urls = ['https://www.linkedin.com/uas/login']
    def __init__(self):
        self.key = self.account[0]
        self.password = self.account[1]
        self.url_login = self.start_urls[0]
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        cap["phantomjs.page.settings.userAgent"] = self.ua
        # self.driver = webdriver.PhantomJS(r'C:\Python27\phantomjs-2.0.0-windows\bin\phantomjs.exe',desired_capabilities=cap,service_args=self.service_args)
        self.driver = webdriver.PhantomJS(r'C:\Python27\phantomjs-2.0.0-windows\bin\phantomjs.exe',desired_capabilities=cap)
        self.timeout = 5


    def start_requests(self):
        return [Request("https://www.linkedin.com/uas/login", callback = self.login)]

    def login(self, response):
        self.driver.get(self.url_login)
        self.driver.find_element_by_id("session_key-login").send_keys(self.key)
        self.driver.find_element_by_id("session_password-login").send_keys(self.password)
        bttn = self.driver.find_element_by_id("btn-primary")
        bttn.click()
        self.driver.maximize_window()
        try:
            time.sleep(random.uniform(2,4))
        except IOError, e:
            free_user_in_mysql(self.key)
        # cookie_list = self.driver.get_cookies()
        # cookie_dict = {}
        # for cookie in cookie_list:
        #     #写入文件
        #     f = open(cookie['name']+'.link','w')
        #     pickle.dump(cookie, f)
        #     f.close()
        #
        #     if cookie.has_key('name') and cookie.has_key('value'):
        #         cookie_dict[cookie['name']] = cookie['value']
        task = []
        while True:
            try:
                time.sleep(random.uniform(1,3))
            except IOError, e:
                free_user_in_mysql(self.key)
            task = get_task_from_mysql()
            if task:
                task_url = task[0]
                task_type = task[1]
                # return cookie_dict
                if task_type == 1:
                    # person
                    try:
                        self.driver.get(task_url)
                        #if user is banned, close the spider
                        if self.driver.current_url == self.url_login:
                            ban_user_from_mysql(self.key)
                            driver.close()
                            sys.exit(0)

                        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "results")))
                        conn = MySQLConnect().getconnect()
                        cur = conn.cursor()
                        cur.execute("""update searchinfo set task_status = 2 where task_status = 1 and url = %s""", task_url)
                        cur.close()
                        conn.commit()
                        conn.close()
                        profilecards = self.driver.find_elements_by_xpath('//ol[@id="results"]/li/a')
                        profileurl = []
                        for profilecard in profilecards:
                            url = profilecard.get_attribute("href")
                            profileurl.append(url)
                        for purl in profileurl:
                            try:
                                time.sleep(random.uniform(2,4))
                            except IOError, e:
                                free_user_in_mysql(self.key)
                            item = self.parse_person_item(self.driver,purl)
                            yield ProfileItem(profile_url=item["profile_url"],profile_img=item["profile_img"],profile_name=item["profile_name"],profile_headline=item["profile_headline"],profile_location=item["profile_location"],profile_industry=item["profile_industry"],profile_current=item["profile_current"],profile_previous=item["profile_previous"],profile_education=item["profile_education"],profile_homepage=item["profile_homepage"],profile_summary_bkgd=item["profile_summary_bkgd"],profile_experience_bkgd=item["profile_experience_bkgd"],profile_honors_bkgd=item["profile_honors_bkgd"],profile_projects_bkgd=item["profile_projects_bkgd"],profile_top_skills_bkgd=item["profile_top_skills_bkgd"],profile_also_knows_bkgd=item["profile_also_knows_bkgd"],profile_education_bkgd=item["profile_education_bkgd"],profile_organizations_bkgd=item["profile_organizations_bkgd"],profile_organizations_supports=item["profile_organizations_supports"],profile_causes_cares=item["profile_causes_cares"],key=self.key)
                    except:
                        pass
                        # yield scrapy.Request(profile, headers=self.headers, cookies=self.cookdic, timeout=self.timeout, callback=self.parse_person_item)
                elif task_type == 2:
                    # company
                    try:
                        self.driver.get(task_url)
                        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "results")))
                        conn = MySQLConnect().getconnect()
                        cur = conn.cursor()
                        cur.execute("""update searchinfo set task_status = 2 where task_status = 1 and url = %s""", task_url)
                        cur.close()
                        conn.commit()
                        conn.close()
                        companycard = self.driver.find_element_by_xpath('//ol[@id="results"]/li[1]/a')
                        company = companycard.get_attribute("href")
                        item = self.parse_company_item(self.driver,company)
                        yield CompanyItem(company_url=item["company_url"],company_name=item["company_name"],company_logo=item["company_logo"],company_img=item["company_img"],company_description=item["company_description"],company_specialties=item["company_specialties"],company_website=item["company_website"],company_industy=item["company_industy"],company_type=item["company_type"],company_headquarters=item["company_headquarters"],company_size=item["company_size"],company_founded=item["company_founded"],key=self.key)
                    except:
                        pass
                else:
                    # school
                    try:
                        self.driver.get(task_url)
                        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "results")))
                        conn = MySQLConnect().getconnect()
                        cur = conn.cursor()
                        cur.execute("""update searchinfo set task_status = 2 where task_status = 1 and url = %s""", task_url)
                        cur.close()
                        conn.commit()
                        conn.close()
                        schoolcard = self.driver.find_element_by_xpath('//ol[@id="results"]/li[1]/a')
                        school = schoolcard.get_attribute("href")
                        print school
                        item = self.parse_school_item(self.driver,school)
                        yield SchoolItem(school_url=item["school_url"],school_name=item["school_name"],school_logo=item["school_logo"],school_img=item["school_img"],school_location=item["school_location"],genarl_information=item["genarl_information"],school_homepage=item["school_homepage"],school_email=item["school_email"],school_type=item["school_type"],contact_number=item["contact_number"],school_year=item["school_year"],school_address=item["school_address"],undergrad_students=item["undergrad_students"],graduate_students=item["graduate_students"],male=item["male"],female=item["female"],faculty=item["faculty"],admitted=item["admitted"],total_population=item["total_population"],graduated=item["graduated"],student_faculty_ratio=item["student_faculty_ratio"],tuition=item["tuition"],school_notables=item["school_notables"],students_live_place=item["students_live_place"],students_live_num=item["students_live_num"],students_work_company=item["students_work_company"],students_work_num=item["students_work_num"],students_do_field=item["students_do_field"],students_do_num=item["students_do_num"],students_studied_subject=item["students_studied_subject"],students_studied_num=item["students_studied_num"],students_skill_field=item["students_skill_field"],students_skill_num=item["students_skill_num"],key=self.key)
                    except:
                        pass


    def get_cookie_from_linkedin(self):

        self.driver.get(self.url_login)
        self.driver.find_element_by_id("session_key-login").send_keys(self.key)
        self.driver.find_element_by_id("session_password-login").send_keys(self.password)
        bttn = self.driver.find_element_by_id("btn-primary")
        bttn.click()
        self.driver.maximize_window()
        time.sleep(random.uniform(2,4))

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


    def get_linkedin_list(self,response):
        import requests
        from bs4 import BeautifulSoup as bs

        # self.cookdic = self.get_cookie()
        url_list = ['http://www.linkedin.com/vsearch/p?keywords=vijay kumar&company=University of Pennsylvania']
        # self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

        #通过数据库字段判断request的url类型 为person 还是school 还是company
        # r = requests.get(url_list[0], headers=self.headers, cookies=self.cookdic, timeout=self.timeout)
        # soup = BeautifulSoup(r.text, 'lxml')
        self.driver.get(url_list[0])
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, "results")))
        profilecards = self.driver.find_elements_by_xpath('//ol[@id="results"]')
        # file = codecs.open('page.html', 'w', encoding='utf-8')
        # file.write(r.text)
        # file.close()

        # profilecards = soup.find_all("li", class_ = "mod result")
        print profilecards
        for profilecard in profilecards:

            print profilecard
            profile = profilecard.div.h3.a.get('href')
            print profilecard
            print profile
            yield scrapy.Request(profile, headers=self.headers, cookies=self.cookdic, timeout=self.timeout, callback=self.parse_person_item)


    def parse_person_item(self,driver,url):
        item = ProfileItem()
        # items = []
        self.driver.get(url)
        try:
            time.sleep(random.uniform(2,4))
        except IOError, e:
            free_user_in_mysql(self.key)
        #item['website'] = None
        try:
            item['profile_url'] = self.driver.current_url
            print item['profile_url']
        except:
            pass

        try:# null
            item['profile_img'] = None
            item['profile_img'] = self.driver.find_element_by_xpath('//div[@class="profile-picture"]//img').get_attribute("src")
        except:
            pass

        try:
            item['profile_name'] = None
            item['profile_name'] = self.driver.find_element_by_xpath('//div[@id="name"]/h1/span/span').text
        except:
            pass

        try:
            item['profile_headline'] = None
            item['profile_headline'] = self.driver.find_element_by_xpath('//div[@id="headline"]/p').text
        except:
            pass

        try:
            item['profile_location'] = None
            item['profile_location'] = self.driver.find_element_by_xpath('//div[@id="location"]/dl/dd[1]/span/a').text
        except:
            pass

        try:
            item['profile_industry'] = None
            item['profile_industry'] = self.driver.find_element_by_xpath('//div[@id="location"]/dl/dd[2]/a').text
        except:
            pass

        try:# []
            item['profile_current'] = []
            currents = self.driver.find_elements_by_xpath('//tr[@id="overview-summary-current"]/td/ol/li')
            for current in currents:
                ss = current.text
                item['profile_current'].append(ss)
        except:
            pass

        try:# []
            item['profile_previous'] = []
            previouses = self.driver.find_elements_by_xpath('//tr[@id="overview-summary-past"]/td/ol/li')
            for previous in previouses:
                ss = previous.text
                item['profile_previous'].append(ss)
        except:
            pass

        try:# []
            item['profile_education'] = []
            educations = self.driver.find_elements_by_xpath('//tr[@id="overview-summary-education"]/td/ol/li')
            for education in educations:
                ss = education.text
                item['profile_education'].append(ss)
        except:
            pass

        try:
            item['profile_homepage'] = None
            item['profile_homepage'] = self.driver.find_element_by_xpath('//dl[@class="public-profile"]/dd/a').text
        except:
            pass

        try:
            item['profile_summary_bkgd'] = None
            item['profile_summary_bkgd'] = self.driver.find_element_by_xpath('//div[@id="summary-item-view"]/div/p').text
        except:
            pass

        try:
            item['profile_experience_bkgd'] = []
            experiences = self.driver.find_elements_by_xpath('//div[@id="background-experience"]/div')
            for experience in experiences:
                ss = experience.text
                item['profile_experience_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_honors_bkgd'] = []
            honors = self.driver.find_elements_by_xpath('//div[@id="background-honors"]/div')
            for honor in honors:
                ss = honor.text
                item['profile_honors_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_projects_bkgd'] = []
            projects = self.driver.find_elements_by_xpath('//div[@id="background-projects"]/div')
            for project in projects:
                ss = project.text
                item['profile_projects_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_top_skills_bkgd'] = []
            skills = self.driver.find_elements_by_xpath('//div[@id="profile-skills"]/ul[1]/li/span/span')
            for skill in skills:
                ss = skill.text
                item['profile_top_skills_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_also_knows_bkgd'] = []
            knows = self.driver.find_elements_by_xpath('//div[@id="profile-skills"]/ul[2]/li/div/span/span')
            for know in knows:
                ss = know.text
                item['profile_also_knows_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_education_bkgd'] = []
            educations_bk = self.driver.find_elements_by_xpath('//div[@id="background-education"]/div')
            for education_bk in educations_bk:
                ss = education_bk.text
                item['profile_education_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_organizations_bkgd'] = []
            organizations = self.driver.find_elements_by_xpath('//div[@id="background-organizations"]/div')
            for organization in organizations:
                ss = organization.text
                item['profile_organizations_bkgd'].append(ss)
        except:
            pass

        try:
            item['profile_organizations_supports'] = []
            organizations_sup = self.driver.find_elements_by_xpath('//div[@id="volunteering-organizations-view"]/div/ul/li')
            for organization_sup in organizations_sup:
                ss = organization_sup.text
                item['profile_organizations_supports'].append(ss)
        except:
            pass

        try:
            item['profile_causes_cares'] = []
            causes = self.driver.find_elements_by_xpath('//div[@id="volunteering-causes-view"]/div/ul/li')
            for cause in causes:
                ss = cause.text
                item['profile_causes_cares'].append(ss)
        except:
            pass

        # items.append(item)

        return item


    def parse_company_item(self,driver,url):
        self.driver.get(url)
        try:
            time.sleep(random.uniform(2,4))
        except IOError, e:
            free_user_in_mysql(self.key)
        item = CompanyItem()
        # sel = Selector(response)
        # items = []
        try:
            more = self.driver.find_element_by_class_name("view-more-bar")
            more.click()
        except:
            pass

        try:
            item['company_url'] = self.driver.current_url
            print item['company_url']
        except:
            pass

        try:
            item['company_name'] = None
            item['company_name'] = self.driver.find_element_by_xpath('//div[@class="left-entity"]/div/h1').text
        except:
            pass

        try:
            item['company_logo'] = None
            item['company_logo'] = self.driver.find_element_by_xpath('//div[@class="image-wrapper"]/img').get_attribute("src")
        except:
            pass

        try:
            item['company_img'] = None
            item['company_img'] = self.driver.find_element_by_xpath('//div[@id="stream-about-section"]/img').get_attribute("src")
        except:
            pass

        try:
            item['company_description'] = None
            item['company_description'] = self.driver.find_element_by_xpath('//div[@class="basic-info-description"]/p').text
        except:
            pass

        try:
            item['company_specialties'] = None
            item['company_specialties'] = self.driver.find_element_by_xpath('//div[@class="specialties"]/p').text
        except:
            pass

        try:
            item['company_website'] = None
            item['company_website'] = self.driver.find_element_by_xpath('//li[@class="website"]/p').text
        except:
            pass

        try:
            item['company_industy'] = None
            item['company_industy'] = self.driver.find_element_by_xpath('//li[@class="industry"]/p').text
        except:
            pass

        try:
            item['company_type'] = None
            item['company_type'] = self.driver.find_element_by_xpath('//li[@class="type"]/p').text
        except:
            pass

        try:
            item['company_headquarters'] = None
            item['company_headquarters'] = self.driver.find_element_by_xpath('//li[@class="vcard hq"]/p').text
        except:
            pass

        try:
            item['company_size'] = None
            item['company_size'] = self.driver.find_element_by_xpath('//li[@class="company-size"]/p').text
        except:
            pass

        try:
            item['company_founded'] = None
            item['company_founded'] = self.driver.find_element_by_xpath('//li[@class="founded"]/p').text
        except:
            pass

        # items.append(item)

        return item


    def parse_school_item(self,driver,url):
        self.driver.get(url)
        try:
            time.sleep(random.uniform(2,4))
        except IOError, e:
            free_user_in_mysql(self.key)
        item = SchoolItem()
        # sel = Selector(response)

        try:
            item['school_url'] = self.driver.current_url
            print item['school_url']
        except:
            pass

        try:
            item['school_name'] = None
            item['school_name'] = self.driver.find_element_by_xpath('//div[@class="header"]/div[1]/div/h1').text
        except:
            pass

        try:
            item['school_location'] = None
            item['school_location'] = self.driver.find_element_by_xpath('//div[@class="header"]/div[1]/div/h4').text
        except:
            pass

        try:
            item['school_logo'] = None
            item['school_logo'] = self.driver.find_element_by_xpath('//div[@class="header"]/a/img').get_attribute("src")
        except:
            pass

        try:
            item['school_img'] = None
            item['school_img'] = self.driver.find_element_by_xpath('//div[@id="college-cover-photo"]//img').get_attribute("src")
        except:
            pass

        try:
            more = self.driver.find_element_by_class_name("view-more-bar")
            more.click()
        except:
            pass

        try:
            item['genarl_information'] = None
            item['genarl_information'] = self.driver.find_element_by_xpath('//dd[@class="full-description"]').text
        except:
            pass

        try:
            item['school_homepage'] = None
            item['school_homepage'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Homepage")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['school_email'] = None
            item['school_email'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Email")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['school_type'] = None
            item['school_type'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Institution Type")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['contact_number'] = None
            item['contact_number'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Phone")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['school_year'] = None
            item['school_year'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Year Level")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['school_address'] = None
            item['school_address'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Address")]/following-sibling::dd[1]').text + self.driver.find_element_by_xpath('//dt[contains(text(),"Address")]/following-sibling::dd[2]').text + self.driver.find_element_by_xpath('//dt[contains(text(),"Address")]/following-sibling::dd[3]').text
        except:
            pass

        try:
            item['undergrad_students'] = None
            item['undergrad_students'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Undergrad Students")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['graduate_students'] = None
            item['graduate_students'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Graduate Students")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['faculty'] = None
            item['faculty'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Faculty")][2]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['total_population'] = None
            item['total_population'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Total Population")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['student_faculty_ratio'] = None
            item['student_faculty_ratio'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Student/Faculty Ratio")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['male'] = None
            item['male'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Male")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['female'] = None
            item['female'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Female")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['admitted'] = None
            item['admitted'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Admitted")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['graduated'] = None
            item['graduated'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Graduated")]/following-sibling::dd[1]').text
        except:
            pass

        try:
            item['tuition'] = None
            item['tuition'] = self.driver.find_element_by_xpath('//dt[contains(text(),"Tuition")]/following-sibling::dd[1]').text + self.driver.find_element_by_xpath('//dt[contains(text(),"Tuition")]/following-sibling::dd[2]').text
        except:
            pass

        try:
            self.driver.find_element_by_link_text('Notables').click()
            try:
                time.sleep(random.uniform(2,4))
            except IOError, e:
                free_user_in_mysql(self.key)
        except:
            pass

        try:
            item['school_notables'] = []
            notables = self.driver.find_elements_by_xpath('//ul[@id="my-feed-post"]/li/div/div[1]/a')
            for notable in notables:
                ss = notable.get_attribute("href")
                item['school_notables'].append(ss)
        except:
            pass

        try:
            self.driver.find_element_by_link_text('Students & Alumni').click()
            try:
                time.sleep(random.uniform(2,4))
            except IOError, e:
                free_user_in_mysql(self.key)
        except:
            pass

        try:
            more = self.driver.find_element_by_class_name("view-more-bar")
            more.click()
        except:
            pass

        try:
            item['students_live_place'] = []
            live_places = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[1]/ul/li')
            ss = ""
            for live_place in live_places:
                ss = live_place.get_attribute("title")
                item['students_live_place'].append(ss)
        except:
            pass

        try:
            item['students_live_num'] = []
            live_num = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[1]/ul/li')
            ss = ""
            for num in live_num:
                ss = num.get_attribute("data-count")
                item['students_live_num'].append(ss)
        except:
            pass

        try:
            item['students_work_company'] = []
            companys = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[2]/ul/li')
            ss = ""
            for company in companys:
                ss = company.get_attribute("title")
                item['students_work_company'].append(ss)
        except:
            pass

        try:
            item['students_work_num'] = []
            work_num = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[2]/ul/li')
            ss = ""
            for num in work_num:
                ss = num.get_attribute("data-count")
                item['students_work_num'].append(ss)
        except:
            pass

        try:
            item['students_do_field'] = []
            do_field = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[3]/ul/li')
            ss = ""
            for field in do_field:
                ss = field.get_attribute("title")
                item['students_do_field'].append(ss)
        except:
            pass

        try:
            item['students_do_num'] = []
            do_num = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[3]/ul/li')
            ss = ""
            for num in do_num:
                ss = num.get_attribute("data-count")
                item['students_do_num'].append(ss)
        except:
            pass

        try:
            item['students_studied_subject'] = []
            subjects = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[4]/ul/li')
            ss = ""
            for subject in subjects:
                ss = subject.get_attribute("title")
                item['students_studied_subject'].append(ss)
        except:
            pass

        try:
            item['students_studied_num'] = []
            studied_num = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[4]/ul/li')
            ss = ""
            for num in studied_num:
                ss = num.get_attribute("data-count")
                item['students_studied_num'].append(ss)
        except:
            pass

        try:
            item['students_skill_field'] = []
            skills = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[5]/ul/li')
            ss = ""
            for skill in skills:
                ss = skill.get_attribute("title")
                item['students_skill_field'].append(ss)
        except:
            pass

        try:
            item['students_skill_num'] = []
            skill_num = self.driver.find_elements_by_xpath('//div[@class="carousel-content"]/ul/li[5]/ul/li')
            ss = ""
            for num in skill_num:
                ss = num.get_attribute("data-count")
                item['students_skill_num'].append(ss)
        except:
            pass

        return item
