import re
#import pandas as pn
import time
from selenium import webdriver
from test11.items import LkischoolItem#, LinkedinItem_detalle
from selenium import webdriver
from string import lower


def get_profile_data(driver,url):
    driver.get(url)
    js="var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    item = LkischoolItem()
    #item = LinkedinItem_detalle()
    print("get in url")
    try:
        
        try:
            more=driver.find_element_by_xpath("//a[@class='view-more-bar']")
            more.click()
            print ("open")
        except:
            pass
        #school_img
        try:
            school_img=driver.find_element_by_class_name("cover-photo").get_attribute("src")
            item["school_img"]=school_img
        except:
            pass        
        #work_direction
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                work_direction = editable_item.find_element_by_xpath('//ul[@class="alumni-co-facets alumni-facets-list"]//ul[@class="buckets-container"]').text
                item["work_direction"] = work_direction
            except:
                pass            
        except:
            pass
        #work_field
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                work_field = editable_item.find_element_by_xpath('//ul[@class="alumni-co-facets alumni-facets-list"]/li[2]/ul[@class="buckets-container"]').text
                item["work_field"] = work_field
            except:
                pass            
        except:
            pass
        #gen_message
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                gen_message = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[1]').text
                item["gen_message"] = gen_message
            except:
                pass            
        except:
            pass
        #website
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                website = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[1]').text
                item["website"] = website
            except:
                pass            
        except:
            pass
        #contact_number
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                contact_number = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[1]/dd[2]').text
                item["contact_number"] = contact_number
            except:
                pass            
        except:
            pass
        #address
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
        #school_year
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                school_year = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[2]/dd[last()]').text
                item["school_year"] = school_year
            except:
                pass            
        except:
            pass
        #school_type
        try:
            editable_item = driver.find_element_by_class_name("about-wrapper")
            try:
                school_type = editable_item.find_element_by_xpath('//div[@class="school-info-wrapper"]/dl/dd[2]/dl[2]/dd[last()-1]').text
                item["school_type"] = school_type
            except:
                pass            
        except:
            pass
        #ts_statistic
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
            js1="var q=document.documentElement.scrollTop=0"
            driver.execute_script(js1)
            try:
                stu=driver.find_element_by_xpath("//ul[@class='higher-ed-nav-menu']/li[3]")
                stu.click()
                print ("open2")
                div = driver.find_element_by_class_name("profiles-wrapper")
                print ("find1")
                name1=div.find_element_by_xpath('//div[1]').text
                print name1
            except:
                pass            
        except:
            pass
        driver.back()
        
        print("success get back")
        return item
        
    except:
        item = {'industry':None,'current_job':None,'job_0':None,'job_1':None,'job_2':None,'job_3':None,'job_4':None,'full_content':None,'skills':None,'skills_2':None,'education_sum':None,'education_tot':None,'personal':None}
        driver.back()
        print("defult get back")
        return item


