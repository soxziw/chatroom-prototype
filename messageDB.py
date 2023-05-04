import pymysql

messageID = 0
dbConnMessage = pymysql.connect("chatGroup.db", check_same_thread=False)
messageCursor =  dbConnMessage.cursor()

# 初始化消息表
# no return
def init(): 
    sql = "drop table if exists MESSAGE"
    print(sql)
    messageCursor.execute(sql)
    sql = '''create table MESSAGE(
                msgID INTEGER not null primary key,
                groupID INTEGER not null,
                userID TEXT not null,
                msg TEXT not null)'''
    print(sql)
    messageCursor.execute(sql)
    dbConnMessage.commit()

# 写消息
# return bool
def write(groupID, msg, optUID):
    global messageID
    sql = f"insert into MESSAGE (msgID, groupID, userID, msg) values({messgaeID}, {groupID}, '{optID}', '{msg}')"
    print(sql)
    try:
        if messageCursor.execute(sql):
            print(f'写消息成功')
            messageID = messageID + 1
            dbConnMessage.commit()  
            return True          
    except:
        print('写消息失败')
        dbConnMessage.rollback()   
        return False

# 获取groupID群聊中的所有消息
# return tuple
def getGMsg(groupID, optUID):
    sql = f"select * from MESSAGE where groupID = {groupID}"
    print(sql)
    messageCursor.execute(sql):
    result = messageCursor.fetchall()
    return result

# 获取groupID群聊中userID的所有消息
# return tuple
def getGMsg(groupID, userID, optUID):
    sql = f"select * from MESSAGE where groupID = {groupID} and userID = {userID}"
    print(sql)
    messageCursor.execute(sql):
    result = messageCursor.fetchall()
    return result

# 获取optUID的所有群聊中包含某子句的所有消息
# return tuple
def getGMsg(subMsg, optUID):
    sql = f"select * from MESSAGE where msg like '%{submsg}%' and exists 
               (select * from GROUP_USER where GROUP_USER.groupID = MESSAGE.groupID
                and GROUP_USER.userID = '{optUID}')"
    print(sql)
    messageCursor.execute(sql):
    result = messageCursor.fetchall()
    return result
    