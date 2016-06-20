# -*- coding: utf-8 -*-
import MySQLdb

def get_task_from_mysql():
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
    cur = conn.cursor()
    print "test point 24"
    cur.execute("begin transaction1")
    cur.execute("select url, task_type, from searchinfo where task_status = 0 for update limit 1")
    cur.execute("update searchinfo set task_status = 1 where task_status = 0 limit 1")
    cur.execute("comit transaction1")
    print "test point 25"
    collect = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    return collect
