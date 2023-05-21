import pymysql
import dbBase

messageID = 0
colName = ['msgID', 'groupID', 'userID', 'msg']

def tuple2dict(tmp):
    result = {}
    for i in range(len(colName)):
        result[colName[i]] = [x[i] for x in tmp]
    return result

# 初始化消息表
# no return
def init(): 
    sql = "drop table if exists MESSAGE"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    sql = '''create table MESSAGE(
                msgID int not null primary key,
                groupID int not null,
                userID varchar(255) not null,
                msg varchar(255) not null)'''
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    dbConnMessage.commit()

# 写消息
# return bool
def write(groupID, msg, optUID):
    global messageID
    sql = f"insert into MESSAGE (msgID, groupID, userID, msg) values({messgaeID}, {groupID}, '{optID}', '{msg}')"
    print(sql)
    try:
        if dbBase.cursorMESSAGE.execute(sql):
            print(f'写消息成功')
            messageID = messageID + 1
            dbConnMessage.commit()  
            return True          
    except:
        print('写消息失败')
        dbConnMessage.rollback()   
        return False

# 获取groupID群聊中的所有消息
# return dict
def getGMsg(groupID, optUID):
    sql = f"select * from MESSAGE where groupID = {groupID}"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchall()
    return tuple2dict(result)

# 获取groupID群聊中userID的所有消息
# return dict
def getGUMsg(groupID, userID, optUID):
    sql = f"select * from MESSAGE where groupID = {groupID} and userID = {userID}"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchall()
    return tuple2dict(result)

# 获取optUID的所有群聊中包含某子句的所有消息
# return dict
def getMsg(subMsg, optUID):
    sql = f"select * from MESSAGE where msg like '%{subMsg}%' and exists (select * from GROUP_USER where GROUP_USER.groupID = MESSAGE.groupID and GROUP_USER.userID = '{optUID}')"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchall()
    return tuple2dict(result)
    