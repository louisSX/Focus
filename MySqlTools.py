import pymysql

class MySqlTools():

    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='pc')

    # 查询数据
    def db_query(self,query_sql):
        cursor = self.db.cursor()
        cursor.execute(query_sql)
        data = cursor.fetchall()
        return data

    # 新增一条数据
    def db_insert(self,insert_sql,args):
        cursor = self.db.cursor()
        sql = insert_sql
        try:
            cursor.execute(sql, args)
            self.db.commit()
            return 1
        except Exception as e:
            self.db.rollback()
            print(e)
            return 0

    # 更新一条数据
    def db_update(self,update_sql,args):
        cursor = self.db.cursor()
        try:
            cursor.execute(update_sql, args)
            self.db.commit()
            return 1
        except Exception as e:
            self.db.rollback()
            print(e)
            return 0

    # 删除数据
    def db_delete(self,delete_sql):
        cursor = self.db.cursor()
        try:
            cursor.execute(delete_sql)
            self.db.commit()
            return 1
        except Exception as e:
            self.db.rollback()
            print(e)
            return 0

    # 关闭数据库连接
    def db_close(self):
        self.db.close()