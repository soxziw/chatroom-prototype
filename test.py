import pymysql

dbConn = pymysql.connect(host='localhost', port=3306, user="root", password="Xjm_20020827", database="test", charset="utf8", autocommit=True)
cursor = dbConn.cursor()
# sql = "drop table if exists User"
# print(sql)
# cursor.execute(sql)

# sql = f"CREATE TABLE User(userID varchar(255) not null, name varchar(255) not null, password varchar(255) not null)"
# print(sql)
# cursor.execute(sql)

# sql = "INSERT IGNORE INTO User(userID, name, password) VALUES(%(userID)s, %(name)s, %(password)s)"
# print(sql)
# print(cursor.execute(sql, {'userID': 'a', 'name': 'b', 'password': 'c',}))

# sql = "INSERT IGNORE INTO User(userID, name, password) VALUES(%(userID)s, %(name)s, %(password)s)"
# print(sql)
# print(cursor.execute(sql, {'userID': 'a', 'name': 'b', 'password': 'c',}))

# # sql = "UPDATE USER SET name = %(name)s WHERE userID = %(optUID)s"
# # print(sql)
# # print(cursor.execute(sql, {'name': 'n', 'optUID': 'b',}))
# # # print(cursor.fetchone()[2])

# sql = "SELECT * FROM USER WHERE userID = %(userID)s"
# print(cursor.execute(sql, {'userID': 'a',}))
# print(cursor.fetchone()[1])

sqllist = open('D:\Program x64\PowerDesigner\chatRoom.sql', 'r').read().split(';')
for sql in sqllist[0:-1]:
    ret = cursor.execute(sql)
    print(sql, " END", ret)