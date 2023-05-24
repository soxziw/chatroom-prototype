import dbBase
    
def apply(userID, optUID):
    sql = "SELECT * FROM FRIENDS WHERE userID = %(optUID)s AND friendID = %(userID)s"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.SELECT.FAIL:
        return True
    sql = "CALL INSERT_FRIEND( %(userID)s,%(optUID)s,'UNSET');"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.INSERT.FAIL:
        return True
    return False

def agree(userID, optUID):
    sql = "SELECT * FROM FRIENDS WHERE (userID = %(optUID)s AND friendID = %(userID)s)"
    status = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    if status != dbBase.SELECT.ONE:
        return False
    sql = "CALL UPDATE_FRIEND(%(optUID)s,%(userID)s,'SET');"
    status1 = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    sql = "CALL INSERT_FRIEND(%(userID)s,%(optUID)s,'SET');"
    status2 = dbBase.cursorFRIENDS.execute(sql, {'userID': userID, 'optUID': optUID,})
    
    if status1 != dbBase.UPDATE.ONE or status2 == dbBase.INSERT.FAIL:
        return False
    return True
    
def getFriends(optUID):
    sql = "SELECT friendID, status FROM FRIENDS WHERE userID = %(optUID)s"
    status = dbBase.cursorFRIENDS.execute(sql, {'optUID': optUID,})
    if status == dbBase.SELECT.FAIL:
        return [{'friendID': '', 'status': ''},]
    result = dbBase.cursorFRIENDS.fetchall()
    friends = []
    for r in result:
        friends.append({'friendID': r[0], 'status': r[1]})
    return friends