import pymysql


# 获取数据库连接
def get_connection():
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'spider01'
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    return db


# 获取数据库游标
def get_cursor(db):
    cursor = db.cursor()
    return cursor


# 关闭数据库连接
def close_connection(db):
    db.close()


# 插入一条数据, item为字典
def insert_record(db, cursor, item):
    sql = "insert into maoyan (actor, movie, rate, releasetime, score, cover) " \
          "values ('%s', '%s', '%s', '%s', '%s', '%s')" % (item['actor'],
                                                           item['movie'],
                                                           item['rate'],
                                                           item['releasetime'],
                                                           item['score'],
                                                           item['cover'])
    # print(sql)
    cursor.execute(sql)
    db.commit()
