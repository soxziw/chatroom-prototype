import dbBase
    
def apply(userID, optUID):
    sql = "SELECT * FROM FRIENDS WHERE userID = %(optUID)s AND friendID = %(userID)s"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.SELECT.FAIL:
        return True
    sql = "INSERT IGNORE INTO FRIENDS(userID, friendID, status) VALUES(%(optUID)s, %(userID)s, 'UNSET')"
    status1 = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    status2 = dbBase.cursorFRIENDS.execute(sql, {'userID': optUID, 'optUID': userID,})
    if status1 != dbBase.INSERT.FAIL and status2 != dbBase.INSERT.FAIL:
        return True
    return False

def agree(userID, optUID):
    sql = "SELECT * FROM FRIENDS WHERE (userID = %(optUID)s AND friendID = %(userID)s) OR (userID = %(userID)s AND friendID = %(optUID)s)"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.SELECT.TWO:
        return False
    sql = "UPDATE FRIENDS SET status = 'SET' WHERE (userID = %(optUID)s AND friendID = %(userID)s) OR (userID = %(userID)s AND friendID = %(optUID)s)"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.UPDATE.TWO:
        return False
    
def getFriends(optUID):
    sql = "SELECT friendID, status FROM FRIENDS WHERE userID = %(optUID)s"
    status = dbBase.cursorFRIENDS.execute(sql, {'optUID': optUID,})
    if status == dbBase.SELECT.FAIL:
        return [{'friendID': '', 'status': ''},]
    result = dbBase.cursorUSER.fetchall()
    friends = []
    for r in result:
        friends.append({'friendID': r[0], 'status': r[1]})
    return friends