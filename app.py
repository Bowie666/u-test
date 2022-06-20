import os

from flask import Flask, jsonify, request
import joblib
import pymysql
from DBUtils.PooledDB import PooledDB


app = Flask(__name__)

if not os.path.isfile('iris-model.model'):
    raise Exception('没有模型')

model = joblib.load('iris-model.model')

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
        create table if not exists iris(
            id int primary key  AUTO_INCREMENT,
            sepal_length CHAR(40),
            sepal_width CHAR(40),
            petal_length CHAR(40),
            petal_width CHAR(40),
            class CHAR(40),
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

@app.route('/predict', methods=['POST'])
def predict():
    posted_data = request.get_json()
    sepal_length = posted_data['sepal_length']

    sepal_width = posted_data['sepal_width']
    petal_length = posted_data['petal_length']
    petal_width = posted_data['petal_width']

    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])[0]
    if prediction == 0:
        predicted_class = 'Iris-setosa'
    elif prediction == 1:
        predicted_class = 'Iris-versicolor'
    else:
        predicted_class = 'Iris-virginica'

    insert_sql = 'insert into iris(sepal_length, sepal_width, petal_length, petal_width, class) values(%s,%s,%s,%s,%s)'
    insert_val = (sepal_length, sepal_width, petal_length, petal_width, str(float(prediction)))

    db.insert_val(insert_sql, insert_val)

    return jsonify({
        'Prediction': predicted_class,
        'prediction': str(prediction)
    })

if __name__ == '__main__':
    # train_model()
    app.run(port=10544)
