from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from linkedincrawl.items import LinkedincrawlItem
from linkedincrawl.configs import LinkedInAccount
from linkedincrawl.spiders.login import linkedin_login
import sys
import string
import scrapy
import urllib
import httplib2
import requests
import Cookie
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )

class LinkedinSpider(Spider):

    name = "linkedincrawl"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["http://www.linkedin.com"]
    account = LinkedInAccount().get()
    # s = "https://www.linkedin.com/vsearch/p?firstName=vijay&lastName=kumar&company=University of Pennsylvania"
    # start_urls.append(s)
    def start_requests(self):
        return [Request("https://www.linkedin.com/uas/login", callback = self.linkedin_login)]
            # idd = sel.xpath('//div[@class="divtable"]/ul/li/a/@href').re(r'Id=L\d{5}')
            # for dd in idd:
            #     ss = "http://219.238.178.49/BaseInfo.asp?%s" % dd
            #     yield scrapy.Request(ss, callback=self.parse_item)
    def linkedin_login(self, response):

        login_get_url = "https://www.linkedin.com/uas/login"

        # Initialize cookies session here.
        session = requests.Session()

        # Get the html on the login page to grab the tokens needed to log in later.
        login_get = session.get(login_get_url, verify=False).text
        soup = BeautifulSoup(login_get, "lxml")
        user = self.account['key']
        pw = self.account['password']
        csrf_param = soup.find(id="loginCsrfParam-login")['value']
        csrf_token = soup.find(id="csrfToken-login")['value']
        source_alias = soup.find(id="sourceAlias-login")['value']

        payload = {
            'isJsEnabled': 'yes',
            'source_app': '',
            'tryCount': '',
            'clickedSuggestion': 'false',
            'session_key': user,
            'session_password': pw,
            'signin': 'Sign In',
            'session_redirect': '',
            'trk': '',
            'loginCsrfParam': csrf_param,
            'fromEmail': '',
            'csrfToken': csrf_token,
            'sourceAlias': source_alias
        }

        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        raw = urllib.urlencode(payload)

        login_post_url = "https://www.linkedin.com/uas/login-submit"


        sessionCookies = session.cookies
        # login_post = session.post(login_post_url, data=raw, cookies=sessionCookies, headers=headers).text
        # soup = BeautifulSoup(login_post, "lxml")
        # f = open("text.txt",'wb')
        # f.write(login_post)
        # f.close()

        return [FormRequest.from_response(login_post_url,
                            formdata = payload,
                            cookies = sessionCookies,
                            headers = headers,
                            callback = self.parse_item
                            )]


    def parse_item(self, response):
        file = codecs.open('page.html', 'w', encoding='utf-8')
        file.write(response.body)
        file.close()
