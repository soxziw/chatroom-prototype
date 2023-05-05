import dbBase
    
def addUsers(groupID, userIDs, optUID):
    sql = "INSERT INTO UG(userID, groupID) VALUES(%(userID)s, %(groupID)s)"
    status = 1
    for userID in userIDs:
        status = status & dbBase.cursorUG.execute(sql, {'userID': userID, 'groupID': groupID,})
    if status == dbBase.INSERT.FAIL:
        return False
    return True

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
    sql = "SELECT userID FROM UG WHERE userID = %(optUID)s"
    status = dbBase.cursorUG.execute(sql, {'optUID': optUID,})
    if status == dbBase.SELECT.FAIL:
        return []
    result = dbBase.cursorUG.fetchall()
    GIDs = []
    for r in result:
        GIDs.append(r[0])
    return GIDs