import dbBase
    
def addUsers(groupID, userIDs, optUID, status):
    sql = "INSERT INTO UG(userID, groupID, status) VALUES(%(userID)s, %(groupID)s, %(status)s)"
    db_status = 1
    for userID in userIDs:
        db_status = db_status & dbBase.cursorUG.execute(sql, {'userID': userID, 'groupID': groupID, 'status': status})
    if db_status == dbBase.INSERT.FAIL:
        return False
    return True

def getStatus(groupID, optUID):
    sql = "SELECT status FROM UG WHERE groupID = %(groupID)s and userID = %(optUID)s"
    status = dbBase.cursorUG.execute(sql, {'groupID': groupID, 'optUID': optUID,})
    if status != dbBase.SELECT.ONE:
        return 'none'
    result = dbBase.cursorUG.fetchone()
    return result[0]

def deleteUser(groupID, userID, optUID):
    sql = "DELETE FROM UG WHERE userID = %(userID)s AND groupID = %(groupID)s"
    status = dbBase.cursorUG.execute(sql, {'userID': userID, 'groupID': groupID,})
    if status == dbBase.DELETE.FAIL:
        return False
    return True

def getUID(groupID):
    sql = "SELECT userID FROM UG WHERE groupID = %(groupID)s"
    status = dbBase.cursorUG.execute(sql, {'groupID': groupID,})
    if status == dbBase.SELECT.FAIL:
        return []
    result = dbBase.cursorUG.fetchall()
    UIDs = []
    for r in result:
        UIDs.append(r[0])
    return UIDs

def getGID(optUID):
    sql = "SELECT groupID FROM UG WHERE userID = %(optUID)s"
    status = dbBase.cursorUG.execute(sql, {'optUID': optUID,})
    if status == dbBase.SELECT.FAIL:
        return []
    result = dbBase.cursorUG.fetchall()
    GIDs = []
    for r in result:
        GIDs.append(r[0])
    return GIDs