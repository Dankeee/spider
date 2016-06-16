# -*- coding: utf-8 -*-
import MySQLdb

def get_key_from_mysql():
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
    cur.execute("select keytype, keywords, company, school from searchinfo where state = 0")
    collect = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return collect
