# -*- coding: utf-8 -*-
#desde workspace
import MySQLdb
import re
import time
from scrapy.selector import Selector
import scrapy
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from linkedin.items import ImageItem, LinkedinItem, LinkedinItem_school, LinkedinItem_company
import pandas as pn
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from linkedin.crawl_linkedin import get_profile_data
from linkedin.getkey import get_key_from_mysql
import sys
import requests
import os


def try_item(x):
    try:
        res = x
    except:
        res = None
    return res



class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]

    start_urls = ['https://www.linkedin.com/uas/login']

    def parse(self, response):
        cap = webdriver.DesiredCapabilities.PHANTOMJS cap["phantomjs.page.settings.resourceTimeout"] = 1000 cap["phantomjs.page.settings.loadImages"] = False 
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        driver = webdriver.PhantomJS(desired_capabilities=cap)

        driver.get(start_urls[0])
        driver.find_element_by_id("session_key-login").send_keys("877371395@qq.com")
        driver.find_element_by_id("session_password-login").send_keys("kk20080504")
        bttn = driver.find_element_by_id("btn-primary")
        bttn.click()
        time.sleep(5)
        try:
            driver.get("https://www.linkedin.com/")
            identity = driver.find_element_by_id("identity")
            name = identity.find_element_by_class_name("name")
            print
            print "success"
            print name
        reload(sys)
        sys.setdefaultencoding('utf-8')
        collection = []
        while True:
            time.sleep(5)
            collection = get_key_from_mysql()
            print collection
            if collection != 0:
                for j in range(len(collection)):

                    keywords = collection[j]['name']
                    print keywords
                    keytype = collection[j]['type']

                    print keytype
                    if keytype == 1:
                        print keywords

                        urls = []
                        print "check 1"
                        #try:
                        DIRURL = "https://www.linkedin.com/vsearch/p?type=people&keywords={0}".format(keywords)
                        driver.get(DIRURL)
                        current_url = driver.current_url
                        if DIRURL[0:50] != current_url[0:50]:
                            driver.close()
                            sys.exit(0)

                        item = LinkedinItem()
                        Iitem = ImageItem()
                        temp = []
                        keyfield = collection[j]['field']
                        if keyfield == 1:
                            item['field'] = 1
                            print "received field1"
                        else:
                            item['field'] = 2
                            print "received field2"

                        print "check 2"

                        '''try:
                            n_profiles = int(re.search("([0-9]*[\.|\,])?([0-9]*[\.|\,])?[0-9]+",\
                                                    driver.find_element_by_xpath('//div[@class="search-info"]').text).group(0)
                                                    .replace(".","").replace(",",""))
                        except:
                            pass'''
                        conn = MySQLdb.connect(
                            host = '127.0.0.1',
                            port = 3306,
                            db = 'linkedindb',
                            user = 'root',
                            passwd = 'bupt123456',
                            )
                        conn.set_character_set('utf8')
                        cur = conn.cursor()
                        cur.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", keywords)
                        cur.close()
                        conn.commit()
                        conn.close()

                        #n_profiles = 1



                        #perfil_dict = {}


                                #url
                        try:
                            perfil = driver.find_element_by_xpath('//li[@class="mod result idx0 people"]')
                            crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                            print crawlurl
                            item["url"] = crawlurl[0:115]
                            urls.append(crawlurl)
                        except:
                            try:
                                perfil = driver.find_element_by_xpath('//li[@class="mod result idx1 people"]')
                                crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                print crawlurl
                                item["url"] = crawlurl[0:115]
                                urls.append(crawlurl)
                            except:
                                pass



                        #name
                        try:
                            name = perfil.find_element_by_class_name("title").text
                            item["name"] = name
                        except:
                            pass



                        #description
                        try:
                            description = perfil.find_element_by_class_name("description").text
                            item["description"] = description
                        except:
                            pass




                        #similar
                        try:
                            similar = perfil.find_element_by_xpath('//li[@class="similar"]//a').get_attribute("href")
                            item["similar"] = similar
                        except:
                            pass



                        #profile_image
                        try:
                            profile_img = perfil.find_element_by_class_name("entity-img").get_attribute("src")
                            item["profile_img_s"] = profile_img#.split('/')[-1]
                            temp.append(profile_img)
                            Iitem["image_urls"] = temp
                            Iitem['images'] = Iitem['image_urls']
                        except:
                            pass

                        #crawl_linked
                        try:
                            #print item["current_job"]
                            items = get_profile_data(driver,crawlurl)
                            item["worked"] = items["worked"]
                            item["education_background"] = items["education_background"]
                            item["location"] = items["location"]
                            item["industry"] = items["industry"]
                            item["current_job"] = items["current_job"]
                            item["job_0"] = items["job_0"]
                            item["job_1"] = items["job_1"]
                            item["job_2"] = items["job_2"]
                            item["job_3"] = items["job_3"]
                            item["job_4"] = items["job_4"]
                            item["full_content"] = items["full_content"]
                            item["skills"] = items["skills"]
                            item["skills_2"] = items["skills_2"]
                            item["education_sum"] = items["education_sum"]
                            item["education_tot"] = items["education_tot"]
                            item["award"] = items["award"]
                            print ("again")
                        except:
                            pass
                        print("out")



                        '''bttn = driver.find_element_by_xpath('//li[@class="next"]//a[@class="page-link"]')
                        bttn.click()
                        time.sleep(5)'''


                        yield LinkedinItem(url=item["url"],name=item["name"],description=item["description"],location=item["location"],similar=item["similar"],profile_img_s=item["profile_img_s"],\
                                                   worked=item["worked"],education_background=item["education_background"],industry=item["industry"],current_job=item["current_job"],job_0=item["job_0"],\
                                                   job_1=item["job_1"],job_2=item["job_2"],job_3=item["job_3"],job_4=item["job_4"],full_content=item["full_content"],skills=item["skills"],skills_2=item["skills_2"],\
                                                   key=keywords,education_sum=item["education_sum"],education_tot=item["education_tot"],award=item["award"],field=item['field'])
                        yield ImageItem(image_urls=Iitem["image_urls"],images=Iitem['images'])
                        #except:
                            #pass
                    elif keytype == 2:
                        try:
                            print keywords

                            urls = []
                            temp = []
                            print "check 1"

                            DIRURL = "https://www.linkedin.com/vsearch/c?type=companies&keywords={0}".format(keywords)
                            #url = "https://www.linkedin.com/company/{0}?trk=top_nav_home".format(keywords)
                            driver.get(DIRURL)
                            current_url = driver.current_url
                            if DIRURL[0:50] != current_url[0:50]:
                                driver.close()
                                sys.exit()
                            keyfield = collection[j]['field']
                            if keyfield == 1:
                                item['field'] = 1
                                print "received field1"
                            else:
                                item['field'] = 2
                                print "received field2"
                            '''try:
                                n_profiles = int(re.search("([0-9]*[\.|\,])?([0-9]*[\.|\,])?[0-9]+",\
                                                            driver.find_element_by_xpath('//div[@class="search-info"]').text).group(0)
                                                            .replace(".","").replace(",",""))
                            except:
                                pass'''
                            conn = MySQLdb.connect(
                                host = '127.0.0.1',
                                port = 3306,
                                db = 'linkedindb',
                                user = 'root',
                                passwd = 'bupt123456',
                                )
                            conn.set_character_set('utf8')
                            cur = conn.cursor()
                            cur.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", keywords)
                            cur.close()
                            conn.commit()
                            conn.close()


                            try:
                                perfil = driver.find_element_by_xpath('//li[@class="mod result idx0 company"]')
                                crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                driver.get(crawlurl)
                                item = LinkedinItem_company()
                                Iitem = ImageItem()
                            except:
                                try:
                                    perfil = driver.find_element_by_xpath('//li[@class="mod result idx1 company"]')
                                    crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                    driver.get(crawlurl)
                                    item = LinkedinItem_company()
                                except:
                                    pass
                            try:
                                bttn = driver.find_element_by_class_name("view-more-bar")
                                bttn.click()
                            except:
                                pass

                            keyfield = collection[j]['field']
                            if keyfield == 1:
                                item['field'] = 1
                                print "received field1"
                            else:
                                item['field'] = 2
                                print "received field2"

                            item["company_url"] = crawlurl[0:65]

                            try:
                                item["company_name"] = None
                                item["company_name"] = driver.find_element_by_class_name("name").text
                                #basic = driver.find_element_by_class_name("left-entity")
                                #item["company_name"] = basic.find_element_by_xpath('//div/h1').text
                                #item["company_field"] = basic.find_element_by_xpath('//div/p[1]').text
                                #item["company_scale"] = basic.find_element_by_xpath('//div/p[3]').text
                            except:
                                pass

                            try:
                                item["company_logo"] = None
                                company_logo = driver.find_element_by_class_name("image").get_attribute("src")
                                item["company_logo"] = company_logo#.split('/')[-1]
                                temp.append(company_logo)
                                Iitem["image_urls"] = temp
                                Iitem['images'] = Iitem['image_urls']
                            except:
                                pass

                            try:
                                item["company_img"] = None
                                item["company_img"] = driver.find_element_by_class_name("hero-img").get_attribute("src")
                            except:
                                pass

                            try:
                                item["introducation"] = None
                                item["introducation"] = driver.find_element_by_class_name("basic-info-description").text
                            except:
                                pass


                            try:
                                item["specialties"] = None
                                item["specialties"] = driver.find_element_by_xpath('//div[@class="specialties"]/p').text
                            except:
                                pass


                            try:
                                item["website"] = None
                                item["website"] = driver.find_element_by_xpath('//div[@class="basic-info-about "]/ul/li[1]/p').text
                            except:
                                pass

                            try:
                                item["company_field"] = None
                                item["company_field"] = driver.find_element_by_xpath('//div[@class="basic-info-about "]/ul/li[2]/p').text
                            except:
                                pass

                            try:
                                item["company_style"] = None
                                item["company_style"] = driver.find_element_by_xpath('//div[@class="basic-info-about "]/ul/li[3]/p').text
                            except:
                                pass

                            try:
                                item["location"] = None
                                item["location"] = driver.find_element_by_class_name("adr").text
                            except:
                                pass

                            try:
                                item["company_scale"] = None
                                item["company_scale"] = driver.find_element_by_xpath('//div[@class="basic-info-about "]/ul/li[5]/p').text
                            except:
                                pass

                            try:
                                item["start_year"] = None
                                item["start_year"] = driver.find_element_by_xpath('//div[@class="basic-info-about "]/ul/li[6]/p').text
                            except:
                                pass

                            try:
                                more = driver.find_element_by_xpath('//a[@class="more"]')
                                more.click()
                            except:
                                pass

                            try:

                                conn = MySQLdb.connect(
                                        host = '127.0.0.1',
                                        port = 3306,
                                        db = 'linkedindb',
                                        user = 'root',
                                        passwd = 'bupt123456',
                                        )
                                conn.set_character_set('utf8')
                                cur = conn.cursor()
                                try:
                                    for num in range(0,5):
                                        person = driver.find_element_by_xpath('//li[@class="mod result idx{0} people"]'.format(num))
                                        string = person.find_element_by_class_name("title").text
                                        tmp = u'insert into searchinfo(name, state, type) values ("'+ string + u'", 0, 1)'
                                        cur.execute(tmp)
                                except:
                                    pass
                                cur.close()
                                conn.commit()
                                conn.close()
                            except:
                                pass

                            yield LinkedinItem_company(company_url=item["company_url"],company_name=item["company_name"],company_field=item["company_field"],company_scale=item["company_scale"],
                                                       company_logo=item["company_logo"],company_img=item["company_img"],introducation=item["introducation"],specialties=item["specialties"],
                                                       key=keywords,website=item["website"],company_style=item["company_style"],location=item["location"],start_year=item["start_year"],field=item['field'])

                        except:
                            pass

                    else:
                        try:
                            print keywords
                            DIRURL = "https://www.linkedin.com/vsearch/e?type=edu&keywords={0}".format(keywords)
                            driver.get(DIRURL)
                            '''try:
                                n_profiles = int(re.search("([0-9]*[\.|\,])?([0-9]*[\.|\,])?[0-9]+",\
                                                            driver.find_element_by_xpath('//div[@class="search-info"]').text).group(0)
                                                            .replace(".","").replace(",",""))
                            except:
                                pass'''
                            temp = []
                            current_url = driver.current_url
                            if DIRURL[0:50] != current_url[0:50]:
                                driver.close()
                                sys.exit()
                            conn = MySQLdb.connect(
                                host = '127.0.0.1',
                                port = 3306,
                                db = 'linkedindb',
                                user = 'root',
                                passwd = 'bupt123456',
                                )
                            conn.set_character_set('utf8')
                            cur = conn.cursor()
                            cur.execute("""update searchinfo set state = 1 where state = 0 and name = %s""", keywords)
                            cur.close()
                            conn.commit()
                            conn.close()
                            try:
                                perfil = driver.find_element_by_xpath('//li[@class="mod result idx0 university"]')
                                crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                driver.get(crawlurl)
                                item = LinkedinItem_school()
                            except:
                                try:
                                    perfil = driver.find_element_by_xpath('//li[@class="mod result idx1 university"]')
                                    crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                    driver.get(crawlurl)
                                    item = LinkedinItem_school()
                                    Iitem = ImageItem()
                                except:
                                    pass
                            js="var q=document.documentElement.scrollTop=500"
                            driver.execute_script(js)

                            try:
                                more=driver.find_element_by_xpath("//a[@class='view-more-bar']")
                                more.click()
                                print ("open")
                            except:
                                pass

                            item["school_url"] = crawlurl[0:75]

                            try:
                                item["school_name"] = None
                                item["school_name"] = driver.find_element_by_class_name("title").text
                            except:
                                pass

                            try:
                                item["school_logo"] = None
                                school_logo = driver.find_element_by_class_name("image").get_attribute("src")
                                item["school_logo"] = school_logo#.split('/')[-1]
                                temp.append(school_logo)
                                Iitem["image_urls"] = temp
                                Iitem['images'] = Iitem['image_urls']
                            except:
                                pass

                            try:
                                item["school_img"] = None
                                item["school_img"] = driver.find_element_by_class_name("cover-photo").get_attribute("src")
                            except:
                                pass

                            try:
                                item["location"] = None
                                item["location"] = driver.find_element_by_class_name("subtitle").text
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    work_direction = editable_item.find_element_by_xpath('//ul[@class="alumni-co-facets alumni-facets-list"]//ul[@class="buckets-container"]').text
                                    item["work_direction"] = work_direction
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    work_field = editable_item.find_element_by_xpath('//ul[@class="alumni-co-facets alumni-facets-list"]/li[2]/ul[@class="buckets-container"]').text
                                    item["work_field"] = work_field
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    gen_message = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[1]').text
                                    item["gen_message"] = gen_message
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    website = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[1]').text
                                    item["website"] = website
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    school_type = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[2]/dd[last()-1]').text
                                    item["school_type"] = school_type
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    contact_number = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[2]').text
                                    item["contact_number"] = contact_number
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    school_year = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[2]/dd[last()]').text
                                    item["school_year"] = school_year
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    address1 = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[3]').text
                                    address2 = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[4]').text
                                    item["address"] = address1+address2
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    ts_statistic = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[3]').text
                                    item["ts_statistic"] = ts_statistic
                                except:
                                    pass
                            except:
                                pass

                            try:
                                editable_item = driver.find_element_by_class_name("about-wrapper")
                                try:
                                    finance_infor = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[4]').text
                                    item["finance_infor"] = finance_infor
                                except:
                                    pass
                            except:
                                pass

                            try:
                                stu=driver.find_element_by_xpath("//ul[@class='higher-ed-nav-menu']/li[3]/a").get_attribute("href")
                                print stu
                                driver.get(stu)
                                print "ok"
                                conn = MySQLdb.connect(
                                        host = '127.0.0.1',
                                        port = 3306,
                                        db = 'linkedindb',
                                        user = 'root',
                                        passwd = 'bupt123456',
                                        )
                                conn.set_character_set('utf8')
                                cur = conn.cursor()
                                print "ok2"
                                div = driver.find_element_by_class_name("profiles-wrapper")
                                print "ok3"
                                try:
                                    for i in range(1,4):
                                        print "name"
                                        name1=div.find_element_by_xpath('//div[@id="my-feed-post"]/div[{0}]//div[@class="profile-info"]/a[@class="title"]'.format(i)).text
                                        print name1
                                        temp=u'insert into searchinfo(name,state,type) values ("'+name1+u'",0,1)'
                                        cur.execute(temp)
                                except:
                                    pass
                                cur.close()
                                conn.commit()
                                conn.close()
                            except:
                                pass

                            yield LinkedinItem_school(school_name=item["school_name"],school_url=item["school_url"],school_logo=item["school_logo"],school_img=item["school_img"],\
                                                    work_direction=item["work_direction"],work_field=item["work_field"],gen_message=item["gen_message"],website=item["website"],\
                                                    contact_number=item["contact_number"],address=item["address"],school_year=item["school_year"],school_type=item["school_type"],\
                                                    key=keywords,ts_statistic=item["ts_statistic"],finance_infor=item["finance_infor"],location=item["location"])
                        except:
                            pass
