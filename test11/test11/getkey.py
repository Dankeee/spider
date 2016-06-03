import MySQLdb

def get_key_from_mysql():
    conn = MySQLdb.connect(
            host = '127.0.0.1',
            port = 3306,
            db = 'linkedindb',
            user = 'root',
            passwd = '',
            )
    cur = conn.cursor()
    cur.execute("select name from searchinfo where state = 0")
    names = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return names
