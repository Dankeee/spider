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
                    # {'key':'chixiang@bupt.edu.cn', 'password':'bupt123456'},
             ]
    # get accounts
    def get(self):
        return self.account[ random.randint(0, len(self.account) - 1) ]

#if __name__ == '__main__':
#    acc = LinkedinAccount()
#    print acc.get()
