import re
import pandas as pn
import time
from selenium import webdriver
from linkedin.items import LinkedinItem#, LinkedinItem_detalle
from selenium import webdriver
from string import lower


def get_profile_data(driver,url):
    driver.get(url)
    item = LinkedinItem()
    #item = LinkedinItem_detalle()
    print("get in url")
    try:
        
        try:
            driver.find_element_by_class_name("more-text").click()
        except:
            pass




   	#worked
        try:
            item["worked"] = None
            item["worked"] = driver.find_element_by_xpath('//tr[@id="overview-summary-past"]/td').text
        except:
            pass        




   	#education
        try:
            item["education_background"] = None
            item["education_background"] = driver.find_element_by_xpath('//tr[@id="overview-summary-education"]/td').text
        except:
            pass
        

   	

   	#industry
        try:
            editable_item = driver.find_element_by_class_name("editable-item")
            try:
                location = editable_item.find_element_by_xpath('//span[@class="locality"]').text
                item["location"] = location
                industry = editable_item.find_element_by_xpath('//dd[@class="industry"]').text
                item["industry"] = industry
            except:
                pass            
        except:
            pass




   	#summary
        try:
            item["full_content"] = None
            full_content = driver.find_element_by_class_name("summary").text
            item["full_content"] = full_content
        except:
            pass

        #current_job
        try:
            item['current_job'] = None
            current = driver.find_elements_by_xpath('//div[@id="background-experience"]//div[@class="editable-item section-item current-position"]')
            string = ""
            for each in current:
                string += each.text
                string += "\n"
            item['current_job'] = string
            if item['current_job'] == "":
                item['current_job'] = None             
        except:
            pass
        
        #past experience
        

        try:
            past = driver.find_elements_by_xpath('//div[@id="background-experience"]//div[@class="editable-item section-item past-position"]')
            item["job_0"] = None
            item["job_1"] = None
            item["job_2"] = None
            item["job_3"] = None
            item["job_4"] = None
        
            i = 0
            for each in past:
                string = each.text
                item["job_{0}".format(i)] = string
                i += 1
                if i>4:
                    break
        except:
            pass

        
        #skills
        try:
            item["skills"] = None
            item["skills_2"] = None
            #item["skills"] = driver.find_element_by_xpath('//ul[@class="skills-section"]/li/span/span').text
            #skills = driver.find_element_by_xpath('//ul[@class="skills-section"]')
            #item["skills"] = skills.find_element_by_class_name("endorse-item-name-text").text
            skills = driver.find_elements_by_xpath('//ul[@class="skills-section"]/li/span/span')
            skill_text = ""            
            for skill in skills:
                skill_text += skill.text
                skill_text += "\n"             
            item["skills"] = skill_text          
            if item["skills"] == "":
                item["skills"] = None  
            #item["skills"] = driver.find_element_by_class_name("skills-section").text
            #item["skills_2"] = driver.find_element_by_xpath('//ul[@class="skills-section compact-view"]/li/div/span/span').text
            #skills2 = driver.find_element_by_xpath('//ul[@class="skills-section compact-view"]')
            #item["skills_2"] = skills2.find_element_by_class_name("endorse-item-name-text").text
            skills2 = driver.find_elements_by_xpath('//ul[@class="skills-section compact-view"]/li/div/span/span')
            skill2_text = ""
            for skill in skills2:
                skill2_text += skill.text
                skill2_text += "\n"
            item["skills_2"] = skill2_text
            if item["skills_2"] == "":
                item["skills_2"] = None             
        except:
            pass

        #education
        try:
            item["education_sum"] = None
            item["education_tot"] = None
            item["education_sum"] = driver.find_element_by_xpath('//tr[@id="overview-summary-education"]/td').text
            educations = driver.find_elements_by_xpath('//div[@id="background-education"]/div')
            education_text = ""
            for education in educations:
                education_text += education.text
                education_text += "\n"            
            item["education_tot"] = education_text
            if item["education_tot"] == "":
                item["education_tot"] = None            
        except:
            pass


        try:
            item["award"] = None
            awards = driver.find_elements_by_xpath('//div[@id="background-honors"]/div[@class="editable-item section-item"]')
            award_text = ""
            for award in awards:
                award_text += award.text
                award_text += "\n"
            item["award"] = award_text
            if item["award"] == "":
                item["award"] = None
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


