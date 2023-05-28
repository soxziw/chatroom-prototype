import pymysql
import dbBase

messageID = 0
colName = ['msgID', 'userID', 'groupID', 'msg']

def tuple2dict(tmp):
    result = {'msgID':[], 'userID':[], 'groupID':[], 'msg':[]}
    for i in range(len(colName)):
        result[colName[i]] = [x[i] for x in tmp]
    return result

# 更新最新消息号
# no return
def refreshMsgID():
    global messageID
    sql = "SELECT MAX(msgID) FROM MESSAGE"
    status = dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchone()
    if result[0]:
        messageID = result[0] + 1
        return
    messageID = 0

# 写消息
# return bool
def writeMsg(groupID, msg, optUID):
    global messageID
    sql = f"insert into MESSAGE (msgID, groupID, userID, msg) values({messageID}, {groupID}, '{optUID}', '{msg}')"
    print(sql)
    try:
        if dbBase.cursorMESSAGE.execute(sql):
            print('写消息成功')
            messageID = messageID + 1
            dbBase.dbConn.commit()  
            return True          
    except:
        print('写消息失败')
        dbBase.dbConn.rollback()   
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
    sql = f"select * from MESSAGE where groupID = {groupID} and userID = '{userID}'"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchall()
    return tuple2dict(result)

# 获取optUID的所有群聊中包含某子句的所有消息
# return dict
def getMsg(subMsg, optUID):
    sql = f"select * from MESSAGE where msg like '%{subMsg}%' and exists (select * from UG where UG.groupID = MESSAGE.groupID and UG.userID = '{optUID}')"
    print(sql)
    dbBase.cursorMESSAGE.execute(sql)
    result = dbBase.cursorMESSAGE.fetchall()
    return tuple2dict(result)
    