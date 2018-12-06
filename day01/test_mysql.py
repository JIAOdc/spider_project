import json
import pymysql


# 读取json文件到数据库
def json_get():
    with open('./c.json', 'r', encoding='utf-8') as f:
        # f.read() 是字符串
        datas = json.loads(f)
        return datas


def database_get():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'spider'
    # 创建连接
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    return db


# 创建游标
def cursor_get(db):
    cursor = db.cursor()
    return cursor


# 写入数据
def insert_record(cursor):
    json_result = json_get()
    flag = 0
    for items in json_result:
        m_name = items['电影名']
        star = items['主演']
        b_time = items['上映时间']
        order_num = items['排名']
        sourse = items['评分']
        img_path = items['封面图路径']
        flag += 1
        sql = "insert into test2 (id,m_name,star,b_time,order_num,sourse,img_path)" \
              " values (%d,'%s','%s','%s','%s','%s','%s')" % (flag, m_name, star, b_time, order_num, sourse, img_path)
        cursor.execute(sql)
    return


# 关闭数据库连接
def close_db(db):
    db.close()


# 主函数
def main():
    db = database_get()
    cursor = cursor_get(db)
    insert_record(cursor)
    db.commit()
    close_db(db)
    print('成功')


if __name__ == '__main__':
    main()