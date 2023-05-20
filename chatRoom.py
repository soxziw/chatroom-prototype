import pymysql
dbConn = pymysql.connect("login.db", check_same_thread=False)
from flask import Flask, request, redirect, render_template 


import groupDB, messageDB, userTab, ugTab, friendsTab

webApp = Flask(__name__) #新增代码

# 记录当前用户
curUserName = ""
curUserID = ""

# 记录当前群聊
curGroupName = ""
curGroupID = ""

'''
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
'''

# 生成群聊选择器
def groupSelectText(group_id_list, curGroupID):
	text = ""
	for group_id in group_id_list:
		group_name = groupDB.getName(group_id)
		text = text + "<option value=\"" + group_name +"\" "
		if group_id == curGroupID:
			text = text + "selected"
		text = text + ">" + group_name + "</option>"
	return text

# 聊天室
@webApp.route("/chatRoom")
def chatRoom():
	global curUserName, curUserID, curGroupName, curGroupID
	print(curUserName, curGroupName)
	group_id_list = ugTab.getGID(curUserID)
	if curGroupName != "":
		msg_dict = messageDB.getGMsg(curGroupID)
		l = len(msg_dict['msg'])
		data = "<div class=\"chatData\">"
		for i in range(l):
			tmp_user = userTab.getUser(msg_dict['userID'][i])
			tmp_user_name = tmp_user['name']
			data = data + f"{tmp_user_name}: {msg_dict['msg'][i]}<br>"
		data = data + "</div>" + """<form method="post" action="/sendAndReturn">
						<p><input type="text" id="message" name="message" value="请输入" maxlength="150" class="message"/></p>
						<p><input type="submit" value="发送"/></p></form>"""  		
	return render_template("ChatRoom.html", userName=curUserName, group=groupSelectText(group_id_list, curGroupID), chatData=data)

# 加载群聊数据
@webApp.route("/loadChatData", methods=('post',))
def loadChatData():
	global curUserID, curGroupName, curGroupID
	curGroupName = request.form["groupName"]
	group_id_list = ugTab.getGID(curUserID)
	curGroupID = group_id_list[request.form["groupID"]]
	return redirect("/chatRoom")

# 跳转到创建群聊网页
@webApp.route("/createGroup") 
def createGroup():
	global curUserID
	friends_dict_list = friendsTab.getFriends(curUserID)
	friends_id_list = []
	for friend in friends_dict_list:
		friend['status'] == 'SET':
		friends_id_list.append(friend['friendID'])
	text = ""
	for friend_id in friends_id_list:
		friend_name = userTab.getUser(friend_id)['name']
		text = text + f"<input type=\"checkbox\" value=\"{friend_id}\" name=\"user\"/>{friend_name}"
	return render_template("CreateGroup.html", userName=curUserName, allUser=text)

# 创建群聊并返回聊天室
@webApp.route("/createAndReturn", methods=('post',))
def createAndReturn():
	global curUserID, curGroupID, curGroupName
	group_name = request.form["newGroupName"]
	group_users_id = request.form.getlist("user")
	group_id = groupDB.build(group_name)
	for user_id in group_users_id:
		ugTab.addUser(group_id, user_id, curUserID)
	curGroupID = group_id
	curGroupName = group_name
	return redirect("/chatRoom")

# 跳转到删除群聊成员网页
@webApp.route("/deleteGroup") 
def deleteGroup():
	global curUserID, curGroupID
	users_id_list = ugTab.getUID(curGroupID)
	for user_id in users_id_list:
		user_name = userTab.getUser(user_id)['name']
		text = text + f"<input type=\"checkbox\" value=\"{user_id}\" name=\"user\"/>{user_name}"
	return render_template("DeleteGroup.html", userName=curUserName, allUser=text)

# 删除群聊成员并返回聊天室
@webApp.route("/deleteAndReturn", methods=('post',))
def deleteAndReturn():
	global curUserID, curGroupID, curGroupName
	group_users_id = request.form.getlist("user")
	for user_id in group_users_id:
		ugTab.deleteUser(curGroupID, user_id, curUserID)
	return redirect("/chatRoom")

# 发送信息并返回聊天室
@webApp.route("/sendAndReturn", methods=('post',))
def sendAndReturn():
	global curGroupID, curUserID
	message = request.form["message"]
	messageDB.writeMsg(curGroupID, message, curUserID)
	return redirect("/chatRoom")

# 搜索全局消息
@webApp.route("/searchMsg", methods=('post',))
def sendAndReturn():
	global curGroupID, curUserID
	subMsg = request.form["search"]
	msg_dict = messageDB.getMsg(subMsg, curUserID)
	l = len(msg_dict['msg'])
	data = "<div class=\"searchData\">"
	for i in range(l):
		tmp_user = userTab.getUser(msg_dict['userID'][i])
		tmp_user_name = tmp_user['name']
		tmp_group_name = groupDB.getName(msg_dict['groupID'][i])
		data = data + f"{tmp_user_name} from {tmp_group_name}: {msg_dict['msg'][i]}<br>"
	data = data + "</div>"
	return render_template("SearchMsg.html", userName=curUserName, searchData=data)

if __name__ == "__main__":
	webApp.run(host="0.0.0.0", port=80, debug=True)
