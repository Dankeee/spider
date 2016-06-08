# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfileItem(scrapy.Item):
    profile_url = scrapy.Field()
    profile_img = scrapy.Field()
    profile_name = scrapy.Field()
    profile_headline = scrapy.Field()
    profile_location = scrapy.Field()
    profile_industry = scrapy.Field()
    profile_current = scrapy.Field()
    profile_previous = scrapy.Field()
    profile_education = scrapy.Field()
    profile_homepage = scrapy.Field()
    profile_summary_bkgd = scrapy.Field()
    profile_experience_bkgd = scrapy.Field()
    profile_honors_bkgd = scrapy.Field()
    profile_projects_bkgd = scrapy.Field()
    profile_top_skills_bkgd = scrapy.Field()
    profile_also_knows_bkgd = scrapy.Field()
    profile_education_bkgd = scrapy.Field()
    profile_organizations_bkgd = scrapy.Field()
    profile_organizations_supports = scrapy.Field()
    profile_causes_cares = scrapy.Field()
    key = scrapy.Field()
    pass


class SchoolItem(scrapy.Item):
    # define the fields for your item here like:
    school_url = scrapy.Field()
    school_name = scrapy.Field()
    school_logo = scrapy.Field()
    school_img = scrapy.Field()
    school_location = scrapy.Field()
    genarl_information = scrapy.Field()
    school_homepage = scrapy.Field()
    school_email = scrapy.Field()
    school_type = scrapy.Field()
    contact_number = scrapy.Field()
    school_year = scrapy.Field()
    school_address = scrapy.Field()
    undergrad_students = scrapy.Field()
    graduate_students = scrapy.Field()
    male = scrapy.Field()
    female = scrapy.Field()
    faculty = scrapy.Field()
    admitted = scrapy.Field()
    total_population = scrapy.Field()
    graduated = scrapy.Field()
    student_faculty_ratio = scrapy.Field()
    tuition = scrapy.Field()
    school_notables = scrapy.Field()
    students_live_place = scrapy.Field()
    students_live_num = scrapy.Field()
    students_work_company = scrapy.Field()
    students_work_num = scrapy.Field()
    students_do_field = scrapy.Field()
    students_do_num = scrapy.Field()
    students_studied_subject = scrapy.Field()
    students_studied_num = scrapy.Field()
    students_skill_field = scrapy.Field()
    students_skill_num = scrapy.Field()
    key = scrapy.Field()
    pass



class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    company_logo = scrapy.Field()
    company_img = scrapy.Field()
    company_description = scrapy.Field()
    company_specialties = scrapy.Field()
    company_website = scrapy.Field()
    company_industy = scrapy.Field()
    company_type = scrapy.Field()
    company_headquarters = scrapy.Field()
    company_size = scrapy.Field()
    company_founded = scrapy.Field()
    key = scrapy.Field()
    pass
