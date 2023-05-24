import pymysql
import dbBase

groupID = 0

# 更新最新群编号
# no return
def refreshGroupID():
    global groupID
    sql = "SELECT MAX(groupID) FROM CHATGROUP"
    status = dbBase.cursorGROUP.execute(sql)
    result = dbBase.cursorGROUP.fetchone()
    if result[0]:
        groupID = result[0] + 1
        return
    groupID = 0
   
# 创建群
# return int
def build(groupName):
    global groupID
    sql = f"insert into CHATGROUP (groupID, groupName) values({groupID}, '{groupName}')"
    print(sql)
    try:
        if dbBase.cursorGROUP.execute(sql):
            print('创建群成功')
            groupID = groupID + 1
            dbBase.dbConn.commit()  
            return groupID - 1         
    except:
        print('创建群失败')
        dbBase.dbConn.rollback()   
        return -1

# 更改群名
# return bool
def changeName(groupID, newName, optUID):
    sql = f"update CHATGROUP set groupName = '{newName}' where groupID = {groupID}"
    print(sql)
    try:
        if dbBase.cursorGROUP.execute(sql):
            print('更改群名成功')
            dbBase.dbConn.commit()  
            return True          
    except:
        print('更改群名失败')
        dbBase.dbConn.rollback()   
        return False

# 获得群名
# return string
def getName(groupID):
    sql = f"select groupName from CHATGROUP where groupID = {groupID}"
    print(sql)
    dbBase.cursorGROUP.execute(sql)
    result = dbBase.cursorGROUP.fetchall()
    assert (len(result) == 1)
    return result[0][0]