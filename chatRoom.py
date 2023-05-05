from flask import Flask,request,redirect,render_template #新增代码。装入Flask

#用户模块，userMag，用户管理
import userMag #载入用户管理模块
import chat

webApp=Flask(__name__) #新增代码

#记录当前用户
global curUserName
curUserName=""

#记录当前群聊
global curGroup
curGroup=""

userMag.init()

@webApp.route("/") #新增代码，对应执行root()函数
def root():
	return redirect("/static/Login.html")

@webApp.route("/getUserState",methods=('post',)) #获得用户状态
def getUserState():
	userName=request.form["userName"]

	#用户名是否存在
	checkState=userMag.UserNameState(userName)

	print(checkState)
	if checkState==True :return '1'
	else: return '0'


@webApp.route("/checkUser",methods=('post',)) #用户登录检查
def checkUser():
	userName=request.form["userName"]
	userPassword=request.form["userPWD"]

	#检查用户名密码正确
	checkState=userMag.UserLogin(userName,userPassword)

	if checkState==True: 
		global curUserName
		curUserName=userName
		print(curUserName)
		return "登录成功！"
	return "用户名或密码错误！"

@webApp.route("/addUser",methods=('post',)) #用户注册
def addUser():
	userName=request.form["userName"]
	userPassword=request.form["userPWD"]

	#检查密码长度&用户名是否存在
	checkState=(len(userPassword)>=8)&(userMag.UserNameState(userName)==False)
	if checkState==False:
		return "用户名或密码不符合要求！"
	
	#添加注册表
	addState=userMag.UserAdd(userName,userPassword)
	if addState==False:return '注册失败！'
	chat.InitUser(userName)
	return "注册成功！"

def groupSelectText(allGroup,curGroup): #生成群聊选择器
	l=len(allGroup)
	text=""
	for num in range(0,l):
		text=text+"<option value=\""+allGroup[num][0]+"\" "
		if allGroup[num][0]==curGroup:
			text=text+"selected"
		text=text+">"+allGroup[num][0]+"</option>"
	return text

@webApp.route("/chatRoom") #聊天室
def chatRoom():
	global curUserName,curGroup
	print(curUserName)
	print(curGroup)
	data=""
	allGroup=chat.ChatUser(curUserName)
	if curGroup!="":
		allData=chat.ChatGroup(curGroup)
		l=len(allData)
		data=data+"<div class=\"chatData\">"
		for n in range(0,l):
			data=data+f"{allData[n][0]}: {allData[n][1]}<br>"
		data=data+"</div>"+"""<form method="post" action="/sendAndReturn">
								<p><input type="text" id="message" name="message" value="请输入" maxlength="150" class="message"/></p>
								<p><input type="submit" value="发送"/></p>
							</form>"""
	return render_template("ChatRoom.html",userName=curUserName,group=groupSelectText(allGroup,curGroup),chatData=data)

@webApp.route("/loadChatData",methods=('post',)) #加载群聊数据
def loadChatData():
	global curGroup
	curGroup=request.form["groupName"]
	return redirect("/chatRoom")

@webApp.route("/createGroup") #跳转到创建群聊网页
def createGroup():
	users=userMag.AllUser()
	l=len(users)
	allUser=""
	for n in range(0,l):
		allUser=allUser+f"<input type=\"checkbox\" value=\"{users[n][0]}\" name=\"user\"/>{users[n][0]}"
	return render_template("CreateGroup.html",userName=curUserName,allUser=allUser)

@webApp.route("/createAndReturn",methods=('post',)) #创建群聊并返回聊天室
def createAndReturn():
	groupname=request.form["newGroupName"]
	chat.InitGroup(groupname)
	alluser=request.form.getlist("user")
	l=len(alluser)
	for n in range(0,l):
		username=alluser[n]
		chat.AddGroup(username,groupname)
	global curGroup
	curGroup=groupname
	return redirect("/chatRoom")

@webApp.route("/sendAndReturn",methods=('post',)) #发送信息并返回聊天室
def sendAndReturn():
	global curGroup,curUserName
	message=request.form["message"]
	chat.SendMessage(curGroup,curUserName,message)
	return redirect("/chatRoom")

if __name__=="__main__": #新增代码
	webApp.run(host="0.0.0.0",port=80,debug=True)
