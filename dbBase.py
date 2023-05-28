import pymysql


class SELECT():
    FAIL = 0
    ONE = 1
    TWO = 2
    
class INSERT():
    FAIL = 0
    ONE = 1
    
class UPDATE():
    FAIL = 0
    ONE = 1
    TWO = 2
    
class DELETE():
    FAIL = 0
    ONE = 1
    

dbConn = pymysql.connect(
    host='localhost', 
    port=3306, 
    user="root", 
    password="Xjm_20020827", 
    database="chat", 
    charset="utf8", 
    autocommit=True)

'''
dbConn = pymysql.connect(
    host='127.0.0.1', 
    port=3306, 
    password="goodluck",
    user="root", 
    database="chat", 
    charset="utf8", 
    autocommit=True)
'''

cursor = dbConn.cursor()
sqllist = open('./chatRoom.sql', 'r').read().split(';')
for sql in sqllist[0:-1]:
    cursor.execute(sql)
cursor.close()

cursorUSER = dbConn.cursor()
cursorGROUP = dbConn.cursor()
cursorMESSAGE = dbConn.cursor()
cursorFRIENDS = dbConn.cursor()
cursorUG = dbConn.cursor()
print(f"[{__name__}] Database init successed")