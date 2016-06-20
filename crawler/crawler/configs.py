import random

# MySQL Config
class MySQLConfigs:
    host = 'localhost'
    username = 'root'
    password = 'bupt123456'
    database  = 'linkedin_profiles'


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


class LinkedInUserAgent(object):
    UserAgent = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
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
#if __name__ == '__main__':
#    acc = LinkedinAccount()
#    print acc.get()
