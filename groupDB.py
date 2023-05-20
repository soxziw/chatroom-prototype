import pymysql

groupID = 0
dbConnGroup = pymysql.connect("chat.db", check_same_thread=False)
groupCursor =  dbConnGroup.cursor()

# 初始化群聊表
# no return
def init(): 
    sql = "drop table if exists GROUP"
    print(sql)
    groupCursor.execute(sql)
    sql = '''create table GROUP(
                groupID int not null primary key,
                groupName varchar(255) not null)'''
    print(sql)
    groupCursor.execute(sql)
    dbConnGroup.commit()

# 创建群
# return int
def build(groupName):
    global groupID
    sql = f"insert into GROUP (groupID, groupName) values({groupID}, '{groupName}')"
    print(sql)
    try:
        if groupCursor.execute(sql):
            print('创建群成功')
            groupID = groupID + 1
            dbConnGroup.commit()  
            return groupID - 1         
    except:
        print('创建群失败')
        dbConnGroup.rollback()   
        return -1

# 更改群名
# return bool
def changeName(groupID, newName, optUID):
    sql = f"update GROUP set groupName = '{newName}' where groupID = {groupID}"
    print(sql)
    try:
        if groupCursor.execute(sql):
            print('更改群名成功')
            dbConnGroup.commit()  
            return True          
    except:
        print('更改群名失败')
        dbConnGroup.rollback()   
        return False

# 获得群名
# return string
def getName(groupID):
    sql = f"select groupName from GROUP where groupID = {groupID}"
    print(sql)
    groupCursor.execute(sql):
    result = messageCursor.fetchall()
    assert (len(result) == 1)
    return result[0][1]