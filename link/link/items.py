# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LinkedinItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class PersonProfileItem(Item):
    _id = Field()
    url = Field()
    name = Field()
    locality = Field()
    industry = Field()
    summary = Field()
    specilities = Field()
    skills = Field()
    interests = Field()
    honors = Field()
    education = Field()
    experience = Field()
    overview_html = Field()
    profile_img_s = Field()
    profile_img_m = Field()
