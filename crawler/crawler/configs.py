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
                    {'key':'goodtime616@sina.com', 'password':'goodtime616'},
                    # {'key':'rowan.king@yandex.com', 'password':'1qaz2!QAZ@'},
                    # {'key':'jackb1988@yandex.com', 'password':'&UJM8ik,'},
             ]
    # get accounts
    def get(self):
        return self.account[ random.randint(0, len(self.account) - 1) ]

#if __name__ == '__main__':
#    acc = LinkedinAccount()
#    print acc.get()
