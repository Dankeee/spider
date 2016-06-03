from scrapy import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from CNAS.items import CNASItem
import sys
import string
import scrapy

class CnasSpider(Spider):
    name = "cnas"

    start_urls = []
    for n in range(1,306):
        s = "http://219.238.178.49/Acc_Search2.asp?Class=L&page=%d" % n
        start_urls.append(s)
    '''for n in range(0,15000):
        s = "%05d" % n
        ss = "http://219.238.178.49/BaseInfo.asp?Id=L%s" % s
        start_urls.append(ss)'''
    '''start_urls = [
                "http://219.238.178.49/BaseInfo.asp?Id=L00003"
        ]'''
    '''rules = (
        Rule(SgmlLinkExtractor(allow=('/BaseInfo.asp')), callback='parse_item', follow=True),
    )'''


    def parse(self,response):
        try:
            sel = Selector(response)
            idd = sel.xpath('//div[@class="divtable"]/ul/li/a/@href').re(r'Id=L\d{5}')
            for dd in idd:
                ss = "http://219.238.178.49/BaseInfo.asp?%s" % dd
                yield scrapy.Request(ss, callback=self.parse_item)
        except:
            pass



    def parse_item(self, response):
        if response:
            item = CNASItem()

            sel = Selector(response)
            """try:
                idd = sel.xpath('//div[@class="divtable"]/ul/li/a/@href').re(r'Id=L\d{5}')
                for dd in idd:
                    ss = "http://219.238.178.49/BaseInfo.asp?%s" % dd
                    yield scrapy.Request(ss, callback=self.parse)
            except:
                pass"""

            items = []
            #item['website'] = None
            try:
                item['url'] = None
                item['url'] = str(response.url)
                print item['url']
                print "SSSSSSSSSSSSSSSSSSSSSSSSSSs"
            except:
                pass

            try:
                item['name'] = None
                item['name'] = sel.xpath('//body/div/div[@class="T1"]/text()').extract()[0]
            except:
                pass

            try:
                item['register_id'] = None
                item['register_id'] = sel.xpath('//table/tr[1]/td/span/text()').extract()[0]
            except:
                pass

            try:
                item['other_name'] = None
                item['other_name'] = sel.xpath('//table/tr[2]/td/span/text()').extract()[0]
            except:
                pass

            try:
                item['contacts'] = None
                item['contacts'] = sel.xpath('//table/tr[3]/td[1]/span/text()').extract()[0]
            except:
                pass

            try:
                item['tel'] = None
                item['tel'] = sel.xpath('//table/tr[3]/td[2]/span/text()').extract()[0]
            except:
                pass

            try:
                item['postalcode'] = None
                item['postalcode'] = sel.xpath('//table/tr[4]/td[1]/span/text()').extract()[0]
            except:
                pass

            try:
                item['fax'] = None
                item['fax'] = sel.xpath('//table/tr[4]/td[2]/span/text()').extract()[0]
            except:
                pass

            try:
                item['website'] = None
                item['website'] = sel.xpath('//table/tr[5]/td[1]/span/a/text()').extract()[0]
            except:
                pass

            try:
                item['email'] = None
                item['email'] = sel.xpath('//table/tr[5]/td[2]/span/text()').extract()[0]
            except:
                pass

            try:
                item['address'] = None
                item['address'] = sel.xpath('//table/tr[6]/td/span/text()').extract()[0]
            except:
                pass

            try:
                item['effective_date'] = None
                item['effective_date'] = sel.xpath('//table/tr[7]/td/span/text()').extract()[0]
                items.append(item)
            except:
                pass
        else:
            print "no response"
        return items
