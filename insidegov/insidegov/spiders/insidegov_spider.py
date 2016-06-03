from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from insidegov.items import InsidegovItem
from scrapy.http import Request
import requests
import sys
import string
import scrapy

class InsidegovSpider(Spider):
    #log.start("log",loglevel='INFO')
    name = "insidegov"
    allowed_domains = ["insidegov.com"]
    download_delay = 5
    start_urls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36)"}
    timeout = 5
    for n in range(1,2):
        s = "http://www.insidegov.com/stories?page=%d" % n
        start_urls.append(s)
    print start_urls

    def start_requests(self):
        print "haha"
        r = requests.get(self.start_urls[0], headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        blogcards = soup.find_all(class_ = "t-txt card-sec-el")
        for blogcard in blogcards:
            item = InsidegovItem()
            blog = blogcard.h1.a.get('href')
            item['blog_headline'] = blogcard.find(class_ = "blog-li-desc-lnk").string
            yield scrapy.Request(blog, headers=self.headers, meta=item, callback=self.parse_item)



    def parse_item(self, response):
        if response:
            item = response.meta

            sel = Selector(response)

            items = []
            #item['website'] = None
            try:
                item['blog_url'] = str(response.url)
                print item['blog_url']
            except:
                pass

            try:
                item['blog_title'] = None
                item['blog_title'] = sel.xpath('//div[@id="blog-header"]/div[2]/h1/text()').extract()
            except:
                pass

            try:
                item['blog_athor'] = None
                item['blog_athor'] = sel.xpath('//div[@id="blog-article"]/div[1]/div/div/div[2]/p/text()').extract() + sel.xpath('//div[@id="blog-article"]/div[1]/div/div/div[2]/p/a/span/text()').extract()
            except:
                pass

            try:
                item['blog_img'] = None
                item['blog_img'] = sel.xpath('//div[@id="blog-article"]/div[1]/div/div/div[2]/div[1]/div/div/div/div/img/@src').extract()
            except:
                pass

            try:
                item['blog_credit'] = None
                a = sel.xpath('//div[@id="blog-article"]/div[1]/div/div/div[2]/div[1]/div/div/div/div/p')
                item['blog_credit'] = a.xpath('string(.)').extract()[0]
            except:
                pass

            try:
                item['blog_content'] = ""
                cards = sel.xpath('//div[@id="blog-article"]/div[1]/div/div/div[2]/div[@class="blog-content card-sec-el"]')
                for card in cards:
                    item['blog_content'] += card.xpath('string(.)').extract()[0]
            except:
                pass
            items.append(item)
        else:
            print "no response"
        return items
