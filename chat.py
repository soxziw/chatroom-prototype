import pymysql
dbConnUser=pymysql.connect("chatUser.db",check_same_thread=False)
dbConnGroup=pymysql.connect("chatGroup.db",check_same_thread=False)

global GroupID, MessageID
GroupID=0
MessageID=0

# User's groups
def InitUser(userName): #初始化用户的群聊表
    sql="drop table if exists "+userName
    print(sql)
    dbConnUser.execute(sql)

    sql=f"create table {userName}(groupID INTEGER not null, groupName TEXT not null)"
    print(sql)
    dbConnUser.execute(sql)
    dbConnUser.commit()

def ChatUser(userName): #得到用户的所有群聊
    sql=f"select groupName from {userName}"
    print(sql)
    cur=dbConnUser.execute(sql)
    tmp=cur.fetchall()
    return tmp

def AddGroup(userName,groupName): #增加群聊到用户的群聊表中
    global GroupID
    sql=f"insert into {userName} (groupID,groupName) values({GroupID},'{groupName}')"
    print(sql)
    dbConnUser.execute(sql)
    dbConnUser.commit()
    GroupID=GroupID+1


# Group's messages  
def InitGroup(groupName): #初始化群聊的消息表
    sql="drop table if exists "+groupName
    print(sql)
    dbConnGroup.execute(sql)

    sql="create table "+groupName+"(messageID INTEGER not null, speaker TEXT not null, message TEXT not null)"
    print(sql)
    dbConnGroup.execute(sql)
    dbConnGroup.commit()

def ChatGroup(groupName): #得到群聊的所有消息
    sql=f"select speaker, message from {groupName}"
    print(sql)
    cur=dbConnGroup.execute(sql)
    tmp=cur.fetchall()
    return tmp

def SendMessage(groupName,userName,message): #增加消息到群聊的消息表中
    global MessageID
    sql=f"insert into {groupName} (messageID,speaker,message) values({MessageID},'{userName}','{message}')"
    print(sql)
    dbConnGroup.execute(sql)
    dbConnGroup.commit()
    MessageID=MessageID+1