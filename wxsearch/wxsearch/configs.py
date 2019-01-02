#coding=utf-8
#set debug mode
DEBUG = True



#set database connect infomation
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root@1234'
HOST = '192.168.1.12'
PORT = '3306'
DATABASE = 'SQServer'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)


SQLALCHEMY_TRACK_MODIFICATIONS = False