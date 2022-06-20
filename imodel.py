from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# from sklearn.externals import joblib
import joblib
import pandas as pd
import os
import pymysql
from DBUtils.PooledDB import PooledDB
import time


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

def train_model():
    # iris_df = datasets.load_iris()

    # x = iris_df.data
    # y = iris_df.target

    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, 'iris.csv')
    # filename = '/Users/bowie/Documents/vsfile/u-test/iris.csv'
    names = ['separ-length','separ-width','petal-length','petal-width','class']
    dataset = pd.read_csv(filename, names=names)
    array = dataset.values
    x = array[:, 0:4]
    y = array[:, 4]
    # ValueError: could not convert string to float: 'setosa'

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    dt = DecisionTreeClassifier().fit(X_train, y_train)
    preds = dt.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    name = 'iris-model-{}.model'.format(int(time.time()))
    joblib.dump(dt, name)

    insert_sql = 'insert into trainmodel(name, project, score) values(%s,%s,%s)'
    insert_val = (name, 'iris', str(accuracy))

    db.insert_val(insert_sql, insert_val)

    print('Model Training Finished.\n\tAccuracy obtained: {}'.format(accuracy))

    return name

if __name__ == '__main__':
    print('Training 开始训练模型')
    res = train_model()
    print(f'Training 结束{res}训练模型')
