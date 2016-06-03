# -*- coding: utf-8 -*-
#desde workspace

import re
import time
from scrapy.selector import Selector
import scrapy
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from test11.items import LkischoolItem#, LinkedinItem_detalle
#import pandas as pn
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from test11.crawl_lkischool import get_profile_data
from test11.getkey import get_key_from_mysql

def try_item(x):
    try:
        res = x
    except:
        res = None
    return res



class linkedinSpider(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "lkischool2"
    allowed_domains = ["https://www.linkedin.com"]

    start_urls = ['https://www.linkedin.com/vsearch/e?type=edu']

    def parse(self, response):
        fp = webdriver.FirefoxProfile(r"C:\Users\xiang\AppData\Roaming\Mozilla\Firefox\Profiles\4lhgcpdi.default")
        driver = webdriver.Firefox(firefox_profile=fp)
        names = []
        while True:
            time.sleep(1)
            names = get_key_from_mysql()
            print
            print names
            print
            if names != 0:
                for j in range(len(names)):
                    keywords = names[j][0]

                    print keywords
                    
                    urls = []       
                    print "check 1"
                    
                    url = "https://www.linkedin.com/vsearch/e?type=edu&keywords={0}".format(keywords)
                              


                    driver.get(url)
                    print "check 2"            

                    n_profiles = 1

                    perfil_dict = {}
                    
                    for i in range(0,n_profiles):
                        n_perfil = i
                        try:
                                
                            #url
                            try:
                                perfil = driver.find_element_by_xpath('//li[@class="mod result idx{0} university"]'.format(i))
                                crawlurl = perfil.find_element_by_class_name("title").get_attribute("href")
                                print crawlurl
                                #id = re.search("id=([0-9]+)",url).group(1)
                                perfil_dict["{0}".format(n_perfil)] = {}
                                perfil_dict["{0}".format(n_perfil)]["school_url"] = crawlurl[0:115]
                                urls.append(crawlurl)
                            except:
                                pass
                                

                                
                            #name
                            try:
                                name = perfil.find_element_by_class_name("title").text
                                perfil_dict["{0}".format(n_perfil)]["school_name"] = name
                                print name
                            except:
                                pass

                            try:
                                location = perfil.find_element_by_class_name("description").text
                                perfil_dict["{0}".format(n_perfil)]["location"] = location
                                print ("check4")
                            except:
                                pass

                            #school_logo
                            try:    
                                profile_img_s = perfil.find_element_by_class_name("entity-img").get_attribute("src")
                                perfil_dict["{0}".format(n_perfil)]["profile_img_s"] = profile_img_s
                            except:
                                pass
                            
                            #crawl_linked
                            try:
                                #print item["current_job"]
                                item = get_profile_data(driver,crawlurl)
                                perfil_dict["{0}".format(n_perfil)]["school_img"] = item["school_img"]
                                perfil_dict["{0}".format(n_perfil)]["work_direction"] = item["work_direction"]
                                perfil_dict["{0}".format(n_perfil)]["work_field"] = item["work_field"]
                                perfil_dict["{0}".format(n_perfil)]["gen_message"] = item["gen_message"]
                                perfil_dict["{0}".format(n_perfil)]["website"] = item["website"]
                                perfil_dict["{0}".format(n_perfil)]["contact_number"] = item["contact_number"]
                                perfil_dict["{0}".format(n_perfil)]["address"] = item["address"]
                                perfil_dict["{0}".format(n_perfil)]["school_year"] = item["school_year"]
                                perfil_dict["{0}".format(n_perfil)]["school_type"] = item["school_type"]
                                perfil_dict["{0}".format(n_perfil)]["ts_statistic"] = item["ts_statistic"]
                                perfil_dict["{0}".format(n_perfil)]["finance_infor"] = item["finance_infor"]
                                print ("again")
                            except:
                                pass
                            print("out")
                            
                        except:
                            break
                                                    


                    for each in perfil_dict.keys():
                        urli = perfil_dict.get(each).get("school_url")
                        namei = perfil_dict.get(each).get("school_name")
                        print namei
                        school_logoi=perfil_dict.get(each).get("profile_img_s")
                        print school_logoi
                        school_imgi=perfil_dict.get(each).get("school_img")
                        print school_imgi
                        work_directioni=perfil_dict.get(each).get("work_direction")
                        print work_directioni
                        work_fieldi=perfil_dict.get(each).get("work_field")
                        print work_fieldi
                        gen_messagei=perfil_dict.get(each).get("gen_message")
                        print gen_messagei
                        websitei=perfil_dict.get(each).get("website")
                        print websitei
                        contact_numberi=perfil_dict.get(each).get("contact_number")
                        print contact_numberi
                        addressi=perfil_dict.get(each).get("address")
                        print addressi
                        school_yeari=perfil_dict.get(each).get("school_year")
                        print school_yeari
                        school_typei=perfil_dict.get(each).get("school_type")
                        print school_typei
                        ts_statistici=perfil_dict.get(each).get("ts_statistic")
                        print ts_statistici
                        finance_infori=perfil_dict.get(each).get("finance_infor")
                        print finance_infori
                        locationi=perfil_dict.get(each).get("location")
                        print locationi
                        
                        yield LkischoolItem(school_name=namei,school_url=urli,school_logo=school_logoi,school_img=school_imgi,\
                                            work_direction=work_directioni,work_field=work_fieldi,gen_message=gen_messagei,website=websitei,\
                                            contact_number=contact_numberi,address=addressi,school_year=school_yeari,school_type=school_typei,\
                                            ts_statistic=ts_statistici,finance_infor=finance_infori,location=locationi)
                    print
                    print len(urls)
                    print
        

