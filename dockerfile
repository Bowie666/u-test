FROM python:3.9

RUN pip3 install sklearn numpy pandas pymysql DBUtils==1.3  -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /mlops