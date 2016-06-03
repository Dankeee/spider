# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LinkedincrawlItem(scrapy.Item):
    profile_url = scrapy.Field()
    profile_img = scrapy.Field()
    profile_name = scrapy.Field()
    profile_headline = scrapy.Field()
    profile_location = scrapy.Field()
    profile_industry = scrapy.Field()
    pass
