import MySQLdb
from crawler.configs import MySQLConnect
from scrapy.exceptions import CloseSpider
def get_user_from_mysql():
    conn = MySQLConnect().getconnect()
    cur = conn.cursor()
    user = []
    try:
        # user_status = 1 :aviliable user; user_status = 2 :collecting user; # user_status = 0 :inaviliable user;
        cur.execute("select user_email, user_password from userinfo where user_status = 1 order by rand() limit 1")
        user = cur.fetchone()
        cur.execute("""update userinfo set user_status = 2 where user_email = %s""", user[0])
        conn.commit()
    except:
        conn.rollback()
    cur.close()
    conn.close()
    return user


def ban_user_from_mysql(email):
    conn = MySQLConnect().getconnect()
    cur = conn.cursor()
    cur.execute("""update userinfo set user_status = 0 where user_email = %s""", email)
    conn.commit()
    cur.close()
    conn.close()


def free_user_in_mysql(email):
    conn = MySQLConnect().getconnect()
    cur = conn.cursor()
    cur.execute("""update userinfo set user_status = 1 where user_email = %s""", email)
    conn.commit()
    cur.close()
    conn.close()
    raise CloseSpider('shutdown by ctrl-c')
