import requests
import json
data1 = {
    'rate': 1,
    # 'sepal_length': 2.0,
    # 'sepal_width': 4.2,
    # 'petal_length': 1.5,
    # 'petal_width': 0.3,
    'sepal_length': 6.0,
    'sepal_width': 3.2,
    'petal_length': 4.5,
    'petal_width': 1.3,
    # 'sepal_length': 5.0,
    # 'sepal_width': 3.2,
    # 'petal_length': 5.5,
    # 'petal_width': 1.3
}

headers = {'content-type': 'application/json'}
# print(requests.post("http://127.0.0.1:5000/dataprocess", data=data1).json())
print(requests.post("http://127.0.0.1:10544/predict", headers=headers, data=json.dumps(data1)).json())