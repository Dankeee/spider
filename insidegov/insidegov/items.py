# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InsidegovItem(scrapy.Item):
    blog_url = scrapy.Field()
    blog_title = scrapy.Field()
    blog_headline = scrapy.Field()
    blog_athor = scrapy.Field()
    blog_img = scrapy.Field()
    blog_credit = scrapy.Field()
    blog_content = scrapy.Field()
    pass
