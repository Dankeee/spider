import random
import MySQLdb



# LinkedIn accounts for simulation
class LinkedInAccount(object):
    account = [
                    {'key':'877371395@qq.com', 'password':'kk20080504'},
                    # {'key':'goodtime616@sina.com', 'password':'goodtime616'},
                    # {'key':'rowan.king@yandex.com', 'password':'1qaz2!QAZ@'},
                    # {'key':'jackb1988@yandex.com', 'password':'&UJM8ik,'},
             ]
    # get accounts
    def get(self):
        return self.account[ random.randint(0, len(self.account) - 1) ]

# LinkedIn useragent for simulation
class LinkedInUserAgent(object):
    UserAgent = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
            # 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0 WebKit'
            # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
            # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
            # 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            # 'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
            # 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
            # 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
            # 'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
            # 'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
            # 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
            # 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
            # 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
            # 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
            ]
    # get accounts
    def get(self):
        return self.UserAgent[ random.randint(0, len(self.UserAgent) - 1) ]

# # LinkedIn proxy
# class LinkedInProxy(object):
#     proxy = [
#                     ['--proxy=127.0.0.1:80'],
#                     # ['--proxy=124.192.8.201:3128'],
#                     # ['--proxy=123.206.64.196:80'],
#                     # ['--proxy=118.144.213.85:3128'],
#                     # ['--proxy=121.69.22.6:8118'],
#                     # ['--proxy=219.141.225.107:80'],
#                     # ['--proxy=124.206.133.227:80'],
#                     # ['--proxy=118.144.156.2:3128'],
#                     # ['--proxy=175.25.176.49:80'],
#                     # ['--proxy=218.241.20.219:80'],
#                     # ['--proxy=211.152.39.234:80'],
#                     # ['--proxy=123.56.28.196:8888'],
#                     # ['--proxy=124.206.119.123:3128'],
#                     # ['--proxy=116.213.105.10:80'],
#                     # ['--proxy=123.125.232.23:80'],
#                     # ['--proxy=210.14.143.155:80'],
#                     # ['--proxy=124.206.167.250:3128'],
#                     # ['--proxy=123.56.187.111:82'],
#              ]
#     # get accounts
#     def get(self):
#         return self.proxy[ random.randint(0, len(self.proxy) - 1) ]


# MySQL Config
class MySQLConnect(object):

    def getconnect(self):
        conn = MySQLdb.connect(
            host = '127.0.0.1',
            port = 3306,
            db = 'linkedin',
            user = 'root',
            passwd = 'bupt123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
            )
        conn.set_character_set('utf8')
        return conn
