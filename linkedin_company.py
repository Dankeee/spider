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
from linkedin.items import LinkedinItem, LinkedinItem_school, LinkedinItem_company
import pandas as pn
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from linkedin.crawl_linkedin import get_profile_data
from linkedin.getkey import get_key_from_mysql

def try_item(x):
    try:
        res = x
    except:
        res = None
    return res


class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedincom"
    allowed_domains = ["https://www.linkedin.com"]

    start_urls = ['https://www.linkedin.com/vsearch/p?']

    def parse(self, response):
        fp = webdriver.FirefoxProfile(r"C:\Users\xiang\AppData\Roaming\Mozilla\Firefox\Profiles\4lhgcpdi.default")
        driver = webdriver.Firefox(firefox_profile=fp)
        #driver.get(start_urls[0])
        
        #driver.find_element_by_id("session_key-login").send_keys("chixiang@bupt.edu.cn")
        #driver.find_element_by_id("session_password-login").send_keys("bupt123456")
        

        #driver.find_element_by_id("session_key-login").send_keys("877371395@qq.com")
        #driver.find_element_by_id("session_password-login").send_keys("kk20080504")
        

        #driver.find_element_by_id("session_key-login").send_keys("scrapya@126.com")
        #driver.find_element_by_id("session_password-login").send_keys("bupt123456")        

        
        #driver.find_element_by_id("session_key-login").send_keys("chxchxc@163.com")
        #driver.find_element_by_id("session_password-login").send_keys("bupt123456")



        #driver.find_element_by_id("session_key-login").send_keys("chxchx0@163.com")
        #driver.find_element_by_id("session_password-login").send_keys("bupt123456")
        

        #bttn = driver.find_element_by_id("btn-primary")
        #bttn.click()
        #time.sleep(5)
            

        print "check 1"
        
        url = "https://www.linkedin.com/vsearch/p?keywords={0}&openAdvancedForm=true".format(keywords)
                  


        driver.get(url)
        print "check 2"            

        n_profiles = int(re.search("([0-9]*[\.|\,])?([0-9]*[\.|\,])?[0-9]+",\
                                    driver.find_element_by_xpath('//div[@class="search-info"]').text).group(0)
                                    .replace(".","").replace(",",""))

            #paginacion
        if n_profiles>=10:
            n_paginas = n_profiles/10
            print n_paginas
            if n_paginas > 50:
                n_paginas = 50
            else:
                pass
        else:
            n_paginas = 1
            
        

        perfil_dict = {}
        
        for i in range(1,n_profiles+1):
            n_perfil = i
            try:
                    
                #url
                try:
                    perfil = driver.find_element_by_xpath('//li[@class="mod result idx0 people"]')
                    crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                    print crawlurl
                    #id = re.search("id=([0-9]+)",url).group(1)
                    perfil_dict["{0}".format(n_perfil)] = {}
                    perfil_dict["{0}".format(n_perfil)]["url"] = crawlurl[0:115]
                    urls.append(crawlurl)
                except:
                    pass
                    

                    
                #name
                try:
                    name = perfil.find_element_by_class_name("title").text
                    perfil_dict["{0}".format(n_perfil)]["name"] = name
                except:
                    pass
                    

                    
                #description
                try:
                    description = perfil.find_element_by_class_name("description").text
                    perfil_dict["{0}".format(n_perfil)]["description"] = description
                except:
                    pass
                    
                

                    
                #similar
                try:
                    similar = perfil.find_element_by_xpath('//li[@class="similar"]//a').get_attribute("href")
                    perfil_dict["{0}".format(n_perfil)]["similar"] = similar
                except:
                    pass



                #profile_image
                try:    
                    profile_img_s = perfil.find_element_by_class_name("entity-img").get_attribute("src")
                    perfil_dict["{0}".format(n_perfil)]["profile_img_s"] = profile_img_s
                except:
                    pass

                #crawl_linked
                try:
                    #print item["current_job"]
                    item = get_profile_data(driver,crawlurl)
                    perfil_dict["{0}".format(n_perfil)]["worked"] = item["worked"]
                    perfil_dict["{0}".format(n_perfil)]["education_background"] = item["education_background"]
                    perfil_dict["{0}".format(n_perfil)]["location"] = item["location"]
                    perfil_dict["{0}".format(n_perfil)]["industry"] = item["industry"]                                
                    perfil_dict["{0}".format(n_perfil)]["current_job"] = item["current_job"]
                    perfil_dict["{0}".format(n_perfil)]["job_0"] = item["job_0"]
                    perfil_dict["{0}".format(n_perfil)]["job_1"] = item["job_1"]
                    perfil_dict["{0}".format(n_perfil)]["job_2"] = item["job_2"]
                    perfil_dict["{0}".format(n_perfil)]["job_3"] = item["job_3"]
                    perfil_dict["{0}".format(n_perfil)]["job_4"] = item["job_4"]
                    perfil_dict["{0}".format(n_perfil)]["full_content"] = item["full_content"]
                    perfil_dict["{0}".format(n_perfil)]["skills"] = item["skills"]
                    perfil_dict["{0}".format(n_perfil)]["skills_2"] = item["skills_2"]
                    perfil_dict["{0}".format(n_perfil)]["education_sum"] = item["education_sum"]
                    perfil_dict["{0}".format(n_perfil)]["education_tot"] = item["education_tot"]
                    perfil_dict["{0}".format(n_perfil)]["award"] = item["award"]
                    print ("again")
                except:
                    pass

                try:
                    bttn = driver.find_element_by_xpath('//li[@class="next"]//a[@class="page-link"]')
                    bttn.click()
                    time.sleep(5)
                except:
                    pass
                print("out")
            except:
                break
                                                

        for each in perfil_dict.keys():
            urli = perfil_dict.get(each).get("url")
            namei = perfil_dict.get(each).get("name")         
            descriptioni = perfil_dict.get(each).get("description")
            locationi = perfil_dict.get(each).get("location")
            similari = perfil_dict.get(each).get("similar")
            profile_img_si = perfil_dict.get(each).get("profile_img_s")
            workedi = perfil_dict.get(each).get("worked")
            education_backgroundi = perfil_dict.get(each).get("education_background")
            industryi = perfil_dict.get(each).get("industry")
            current_jobi = perfil_dict.get(each).get("current_job")
            job_0i = perfil_dict.get(each).get("job_0")
            job_1i = perfil_dict.get(each).get("job_1")
            job_2i = perfil_dict.get(each).get("job_2")
            job_3i = perfil_dict.get(each).get("job_3")
            job_4i = perfil_dict.get(each).get("job_4")
            full_contenti = perfil_dict.get(each).get("full_content")
            skillsi = perfil_dict.get(each).get("skills")
            skills_2i = perfil_dict.get(each).get("skills_2")
            education_sumi = perfil_dict.get(each).get("education_sum")
            education_toti = perfil_dict.get(each).get("education_tot")
            awardi = perfil_dict.get(each).get("award")
            
            yield LinkedinItem(url=urli,name=namei,description=descriptioni,location=locationi,similar=similari,profile_img_s=profile_img_si,\
                               worked=workedi,education_background=education_backgroundi,industry=industryi,current_job=current_jobi,job_0=job_0i,\
                               job_1=job_1i,job_2=job_2i,job_3=job_3i,job_4=job_4i,full_content=full_contenti,skills=skillsi,skills_2=skills_2i,\
                               key=keywords,education_sum=education_sumi,education_tot=education_toti,award=awardi)

        print
        print len(urls)
        print

'''
class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedincom"
    allowed_domains = ["https://www.linkedin.com"]

    start_urls = ['https://www.linkedin.com/vsearch/c?']

    def parse(self, response):
        fp = webdriver.FirefoxProfile(r"C:\Users\xiang\AppData\Roaming\Mozilla\Firefox\Profiles\4lhgcpdi.default")
        driver = webdriver.Firefox(firefox_profile=fp)

        names = []
        """while True:
            time.sleep(1)
            names = get_key_from_mysql()
            print
            print names
            print
            if names != 0:
                for j in range(len(names)):"""
        keywords = "ibm"

        print keywords
        
        urls = []       
        print "check 1"

        url = "https://www.linkedin.com/company/{0}?trk=top_nav_home".format(keywords)
                  
        driver.get(url)
        item = LinkedinItem_company()
        try:
            bttn = driver.find_element_by_class_name("view-more-bar")
            bttn.click()
        except:
            pass

        item["company_url"] = url
        
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
            item["company_logo"] = driver.find_element_by_class_name("image").get_attribute("src")
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
                                   website=item["website"],company_style=item["company_style"],location=item["location"],start_year=item["start_year"])
'''
