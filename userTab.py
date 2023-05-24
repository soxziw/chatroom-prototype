import dbBase
    
def getUser(userID):
    sql = "SELECT * FROM USER WHERE userID = %(userID)s"
    status = dbBase.cursorUSER.execute(sql, {'userID': userID,})
    if status != dbBase.SELECT.ONE:
        return {'userID': '', 'name': '', 'password': ''}
    result = dbBase.cursorUSER.fetchone()
    return {'userID': result[0], 'name': result[1], 'password': result[2]}
    
def register(userID, name, password):
    sql = "CALL REGISTER_USER(%(userID)s,%(name)s,%(password)s);"
    status = dbBase.cursorUSER.execute(sql, {'userID': userID, 'name': name, 'password': password,})
    if status != dbBase.INSERT.ONE:
        return False
    return True

def login(userID, password):
    sql = "SELECT password FROM USER WHERE userID = %(userID)s"
    status = dbBase.cursorUSER.execute(sql, {'userID': userID,})
    if status != dbBase.SELECT.ONE:
        return False
    if password != dbBase.cursorUSER.fetchone()[0]:
        return False
    return True

def changeName(name, optUID):
    sql = "CALL UPDATE_USER(%(name)s,%(userID)s);"
    status = dbBase.cursorUSER.execute(sql, {'name': name, 'userID': optUID,})
    if status != dbBase.UPDATE.ONE:
        return False
    return True