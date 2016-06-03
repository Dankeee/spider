from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import log
from link.items import LinkedinItem, PersonProfileItem
from os import path
from link.parser.HtmlParser import HtmlParser
import os
import urllib
import string
from bs4 import UnicodeDammit

class LinkedinspiderSpider(CrawlSpider):
    name = 'LinkedinSpider'
    allowed_domains = ['linkedin.com']
    start_urls = [ "http://www.linkedin.com/directory/people/%s.html" % s 
                   for s in "abcdefghijklmnopqrstuvwxyz" ]

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        pass
        
    def parse(self, response):
        """
        default parse method, rule is not useful now
        """
        response = response.replace(url=HtmlParser.remove_url_parameter(response.url))
        hxs = HtmlXPathSelector(response)
        index_level = self.determine_level(response)
        if index_level in [1, 2, 3, 4]:
            relative_urls = self.get_follow_links(index_level, hxs)
            if relative_urls is not None:
                for url in relative_urls:
                    yield Request(url, callback=self.parse)
        elif index_level == 5:
            personProfile = HtmlParser.extract_person_profile(hxs)
            linkedin_id = self.get_linkedin_id(response.url)
            linkedin_id = UnicodeDammit(urllib.unquote_plus(linkedin_id)).markup
            if linkedin_id:
                personProfile['_id'] = linkedin_id
                personProfile['url'] = UnicodeDammit(response.url).markup
                yield personProfile
    
    def determine_level(self, response):
        """
        determine the index level of current response, so we can decide wether to continue crawl or not.
        level 1: people/[a-z].html
        level 2: people/[A-Z][\d+].html
        level 3: people/[a-zA-Z0-9-]+.html
        level 4: search page, pub/dir/.+
        level 5: profile page
        """
        import re
        url = response.url
        if re.match(".+/[a-z]\.html", url):
            return 1
        elif re.match(".+/[A-Z]\d+.html", url):
            return 2
        elif re.match(".+/people/[a-zA-Z0-9-]+.html", url):
            return 3
        elif re.match(".+/pub/dir/.+", url):
            return 4
        elif re.match(".+/search/._", url):
            return 4
        elif re.match(".+/pub/.+", url):
            return 5
        return None
    
    def get_linkedin_id(self, url):
        find_index = url.find("linkedin.com/")
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None
        
        
    def get_follow_links(self, level, hxs):
        if level in [1, 2, 3]:
            relative_urls = hxs.select("//ul[@class='directory']/li/a/@href").extract()
            relative_urls = ["http://linkedin.com" + x for x in relative_urls]
            return relative_urls
        elif level == 4:
            relative_urls = relative_urls = hxs.select("//ol[@id='result-set']/li/h2/strong/a/@href").extract()
            relative_urls = ["http://linkedin.com" + x for x in relative_urls]
            return relative_urls

            
