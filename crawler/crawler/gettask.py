# -*- coding: utf-8 -*-
import MySQLdb
from crawler.configs import MySQLConnect
def get_task_from_mysql():
    conn = MySQLConnect().getconnect()
    cur = conn.cursor()
    collect = []
    try:
        cur.execute("select url, task_type from searchinfo where task_status = 0 limit 1")
        collect = cur.fetchone()
        #task_status = 0 : uncollect; task_status = 1 : undercollecting; task_status = 2 : collected;
        cur.execute("""update searchinfo set task_status = 1 where url = %s""", collect[0])
        conn.commit()
    except:
        conn.rollback()
    cur.close()
    conn.close()
    return collect
