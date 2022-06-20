import pymysql
from DBUtils.PooledDB import PooledDB
import os

class SQLConn(object):
    def __init__(self):
        self.Pool = PooledDB(
                        creator=pymysql, mincached=2, maxcached=10,maxshared=3, 
                        maxconnections=6, blocking=True,
                        host="146.56.199.55",
                        port=3306,
                        user="root",
                        password="12345678",
                        database="mlops",
                        charset='utf8')

        self.create_table()

    def create_table(self):
        table_sql = """
        create table if not exists trainmodel(
            id int primary key  AUTO_INCREMENT,
            name CHAR(60),
            project CHAR(60),
            score CHAR(40),
            create_time timestamp DEFAULT CURRENT_TIMESTAMP);
        """
        cur, conn = self.get_connect()
        cur.execute(table_sql)
        cur.close()
        conn.close()

    def get_connect (self):
        conn = self.Pool.connection()
        cur = conn.cursor()
        if not cur:
            raise Exception("数据库连接错误")
        else:
            return cur, conn
    
    def insert_val(self, sql, val):
        cur, conn = self.get_connect()
        try:
            cur.execute(sql, val)
            conn.commit()
        except Exception as e:
            # 操作有误时回滚操作
            print("执行===Sql->{}--{}有错，错误是{}，需要回滚".format(sql, val, e))
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def query_sql(self, sql):
        cur, conn = self.get_connect()
        cur.execute(sql)
        req = cur.fetchall()
        # if is a1l:
        cur.close()
        conn.close()
        return req

db = SQLConn()


sql = "select name, score from trainmodel order by id desc;"

res = db.query_sql(sql)
# print(res)  # (('iris-model-1646993517.model', '0.9487179487179487'),)

# 加一个选择逻辑
model_name = res[0][0]
print(model_name) # (('iris-model-1646993517'))
os.system(f'aws s3 cp s3://amlops/iris/{model_name} /home/ec2-user/u-test/iris-model.model')
