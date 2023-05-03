import pymysql
dbConn=pymysql.connect("login.db",check_same_thread=False)

def init():
	sql="drop table if exists userTable"
	print(sql)
	dbConn.execute(sql)
	
	sql="""create table userTable(
            userName TEXT not null,
			userPassword TEXT not null
            )"""
	print(sql)
	dbConn.execute(sql)
	dbConn.commit()

def AllUser():
    sql=f"select userName from userTable"
    print(sql)
    cur=dbConn.execute(sql)
    tmp=cur.fetchall()
    return tmp

#获得用户状态，比如：判断用户是否已经注册
def UserNameState(userName):
	sql=f"select * from userTable where userName='{userName}'"
	print(sql)
	cur=dbConn.execute(sql)
	checkState=cur.fetchone()
	if checkState==None:return False
	return True#表明该用户已经存在

#获得用户密码状态，比如：判断用户名密码是否匹配
def UserLogin(userName,userPassword):
	sql=f"select * from userTable where userName='{userName}' and userPassword='{userPassword}'"
	print(sql)
	cur=dbConn.execute(sql)
	checkState=cur.fetchone()
	if checkState==None:return False
	return True#表明用户名密码正确

#在用户名合规后，真实增加到数据
def UserAdd(userName,userPassword):
	sql=f"insert into userTable (userName,userPassword) values('{userName}','{userPassword}')"
	print(sql)
	try:
		cur=dbConn.execute(sql)
		dbConn.commit() #物理写入数据库
	except:
		return False #发生异常，则返回False

	return True#表明数据库存入成功