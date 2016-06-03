# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class LinkedinItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()    
    location = scrapy.Field()
    similar = scrapy.Field()
    profile_img_s = scrapy.Field()
    industry = scrapy.Field()
    skills_2 = scrapy.Field()
    skills = scrapy.Field()
    current_job =scrapy.Field()
    job_0 = scrapy.Field()
    job_1 = scrapy.Field()
    job_2 = scrapy.Field()
    job_3 = scrapy.Field()
    job_4 = scrapy.Field()
    education_sum = scrapy.Field()
    education_tot = scrapy.Field()
    full_content = scrapy.Field()
    award = scrapy.Field()
    key = scrapy.Field()
    prodication_0 = scrapy.Field()
    prodication_1 = scrapy.Field()
    prodication_2 = scrapy.Field()
    worked = scrapy.Field()
    education_background = scrapy.Field()
    field = scrapy.Field()
    pass


class LinkedinItem_school(scrapy.Item):
    # define the fields for your item here like:
    school_url = scrapy.Field()
    school_name = scrapy.Field()
    school_logo = scrapy.Field()
    school_img = scrapy.Field()
    location = scrapy.Field()
    work_direction = scrapy.Field()
    work_field = scrapy.Field()
    gen_message = scrapy.Field()
    website = scrapy.Field()
    school_type = scrapy.Field()
    contact_number = scrapy.Field()
    school_year = scrapy.Field()
    address = scrapy.Field()
    ts_statistic = scrapy.Field()
    finance_infor = scrapy.Field()
    key = scrapy.Field()
    pass



class LinkedinItem_company(scrapy.Item):
    # define the fields for your item here like:
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    company_logo = scrapy.Field()
    company_img = scrapy.Field()
    company_scale = scrapy.Field()
    introducation = scrapy.Field()
    company_field = scrapy.Field()
    specialties = scrapy.Field()
    website = scrapy.Field()
    company_style = scrapy.Field()
    location = scrapy.Field()
    start_year = scrapy.Field()
    key = scrapy.Field()
    field = scrapy.Field()
    pass


