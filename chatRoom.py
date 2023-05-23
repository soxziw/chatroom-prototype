from glob import glob
from flask import Flask, request, redirect, render_template 
import groupTab, messageTab, userTab, ugTab, friendsTab

webApp = Flask(__name__) #新增代码

# 记录当前用户
curUserName = ""
curUserID = ""

# 记录当前群聊
curGroupName = ""
curGroupID = ""


@webApp.route("/") #新增代码，对应执行root()函数
def root():
    global curUserName, curGroupName
    curUserName = ""
    curGroupName = ""
    return redirect("/static/userLogin.html")

@webApp.route("/login",methods=('post',))
def login():
    userID = request.form["userID"]
    userPassword = request.form["userPassword"]
    checkState = userTab.login(userID, userPassword)

    if checkState == True: 
        global curUserID
        global curUserName
        curUserID = userID
        curUserName = userTab.getUser(userID)['name']
        print(curUserID)
    return [checkState,]

@webApp.route("/register",methods=('post',))
def register():
    userID = request.form["userID"]
    userName = request.form["userName"]
    userPassword = request.form["userPassword"]
    checkState = userTab.register(userID, userName, userPassword)

    if checkState == True: 
        print(curUserID)
    return [checkState,]


@webApp.route("/changeName",methods=('post',))
def changeName():
    global curUserID
    if curUserID == "":
        return [False,]
    userName = request.form["userName"]
    checkState = userTab.changeName(userName, curUserID)

    if checkState == True: 
        global curUserName
        curUserName = userName
        print(userName)
    return [checkState,]


# 生成群聊选择器
def groupSelectText(group_id_list, curGroupID):
	text = ""
	for cnt, group_id in enumerate(group_id_list):
		group_name = groupTab.getName(group_id)
		text = text + f"<option cnt={cnt} value=\"" + group_name + "\" "
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
    chatData = ""
    otherData = ""
    if curGroupName != "":
        msg_dict = messageTab.getGMsg(curGroupID, curUserID)
        print ("msg_dict:", msg_dict)
        l = len(msg_dict['msg'])
        for i in range(l):
            tmp_user = userTab.getUser(msg_dict['userID'][i])
            print("tmp_user", tmp_user)
            tmp_user_name = tmp_user['name']
            chatData = chatData + f"<i class=\"fas fa-comment\"></i> {tmp_user_name}: {msg_dict['msg'][i]}<br>"
        otherData = otherData + """<form method="post" action="/sendAndReturn">
                        <p><input type="text" id="message" name="message" value="请输入" maxlength="150" class="message"/></p>
                        <p><button type="submit"><i class="fas fa-paper-plane"></i>发送</button></form>
                        """
        if ugTab.getStatus(curGroupID, curUserID) == 'high':
            otherData = otherData + "<button id='deleteGroup'><i class=\"fas fa-user-times\"></i>踢人</button>"
        otherData = otherData + "<button id='addGroup'><i class=\"fas fa-user-plus\"></i>加人</button>"
    return render_template("ChatRoom.html", userName=curUserName, group=groupSelectText(group_id_list, curGroupID), chatData=chatData, otherData=otherData)

# 加载群聊数据
@webApp.route("/loadChatData", methods=('post',))
def loadChatData():
    global curUserID, curGroupName, curGroupID
    curGroupName = request.form["groupName"]
    group_id_list = ugTab.getGID(curUserID)
    # print("curGroupName:", curGroupName, "group_id_list:", group_id_list, "groupID:", request.form["groupID"])
    curGroupID = group_id_list[int(request.form["groupID"])]
    return redirect("/chatRoom")

# 跳转到创建群聊网页
@webApp.route("/createGroup") 
def createGroup():
    global curUserID
    friends_dict_list = friendsTab.getFriends(curUserID)
    friends_id_list = []
    for friend in friends_dict_list:
        if friend['status'] == 'SET':
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
    group_id = groupTab.build(group_name)
    ugTab.addUsers(group_id, [curUserID], curUserID, 'high')
    ugTab.addUsers(group_id, group_users_id, curUserID, 'low')
    curGroupID = group_id
    curGroupName = group_name
    return redirect("/chatRoom")

# 跳转到删除群聊成员网页
@webApp.route("/deleteGroup") 
def deleteGroup():
    global curUserID, curGroupID, curGroupName
    users_id_list = ugTab.getUID(curGroupID)
    text = ""
    for user_id in users_id_list:
        user_name = userTab.getUser(user_id)['name']
        text = text + f"<input type=\"checkbox\" value=\"{user_id}\" name=\"user\"/>{user_name}"
    return render_template("DeleteGroup.html", userName=curUserName, groupName=curGroupName, allUser=text)

# 删除群聊成员并返回聊天室
@webApp.route("/deleteAndReturn", methods=('post',))
def deleteAndReturn():
    global curUserID, curGroupID, curGroupName
    if curGroupName == "":
        return redirect("/chatRoom")
    group_users_id = request.form.getlist("user")
    for user_id in group_users_id:
        ugTab.deleteUser(curGroupID, user_id, curUserID)
        if user_id == curUserID:
            curGroupName = ""
    return redirect("/chatRoom")

# 跳转到添加群聊成员网页
@webApp.route("/addGroup") 
def addGroup():
    global curUserID, curGroupID, curGroupName
    friends_dict_list = friendsTab.getFriends(curUserID)
    friends_id_list = []
    for friend in friends_dict_list:
        if friend['status'] == 'SET':
            friends_id_list.append(friend['friendID'])
    text = ""
    for friend_id in friends_id_list:
        # 已经在组里了，不能重复添加
        if ugTab.getStatus(curGroupID, friend_id) != 'none':
            continue
        friend_name = userTab.getUser(friend_id)['name']
        text = text + f"<input type=\"checkbox\" value=\"{friend_id}\" name=\"user\"/>{friend_name}"
    return render_template("AddGroup.html", userName=curUserName, groupName=curGroupName, allUser=text)

# 添加群聊成员并返回聊天室
@webApp.route("/addAndReturn", methods=('post',))
def addAndReturn():
    global curUserID, curGroupID, curGroupName
    group_users_id = request.form.getlist("user")
    ugTab.addUsers(curGroupID, group_users_id, curUserID, 'low')
    return redirect("/chatRoom")

# 发送信息并返回聊天室
@webApp.route("/sendAndReturn", methods=('post',))
def sendAndReturn():
    global curGroupID, curUserID
    message = request.form["message"]
    messageTab.writeMsg(curGroupID, message, curUserID)
    return redirect("/chatRoom")

# 搜索全局消息
@webApp.route("/searchMsg", methods=('post',))
def searchMsg():
    global curGroupID, curUserID
    subMsg = request.form["search"]
    msg_dict = messageTab.getMsg(subMsg, curUserID)
    l = len(msg_dict['msg'])
    data = "<div class=\"searchData\">"
    for i in range(l):
        tmp_user = userTab.getUser(msg_dict['userID'][i])
        tmp_user_name = tmp_user['name']
        tmp_group_name = groupTab.getName(msg_dict['groupID'][i])
        data = data + f"<i class=\"fas fa-comment\"></i> {tmp_user_name} from {tmp_group_name}: {msg_dict['msg'][i]}<br>"
    data = data + "</div>"
    return render_template("SearchMsg.html", userName=curUserName, searchData=data)


@webApp.route("/applyFriends", methods=('post',))
def applyFriends():
    global curUserID
    if curUserID == "":
        return [False,]
    userID = request.form["userID"]
    checkState = friendsTab.apply(userID, curUserID)

    if checkState == True: 
        print(userID)
    return [checkState,]

@webApp.route("/agreeFriends", methods=('post',))
def agreeFriends():
    userID = request.form["userID"]
    global curUserID
    if curUserID == "" or curUserID == userID:
        return [False,]
    checkState = friendsTab.agree(userID, curUserID)

    if checkState == True: 
        print(userID)
    return [checkState,]

@webApp.route("/newFriends")
def newFriends():
    global curUserID
    print(curUserID)
    allFriends = friendsTab.getFriends(curUserID)
    appData = f"<div class='chatData'>"
    for friend in allFriends:
        if friend['status'] == "UNSET":
            FID = friend['friendID']
            appData = appData + f"<div type='text' id='app_{FID}'>{FID}</div><button id='agree_{FID}'>同意</button><br>"
            appData = appData +"""<script type="text/javascript">
                                    $("#agree_""" + FID + """").click(function(){
                                        var userID = $("#app_""" + FID + """").text();
                                        alert(userID);
                                        $.post("/agreeFriends",{userID:userID},function(rtn,){
                                            if (rtn=="true") {
                                                alert("添加好友成功！");
                                                location.reload();
                                            } else {
                                                alert("添加好友失败！");
                                            }
                                        });
                                    });
                                </script>"""
    appData = appData + "</div>"
    userName = userTab.getUser(curUserID)['name']
    return render_template("NewFriends.html", userName = userName, appData = appData)

if __name__=="__main__": #新增代码
    webApp.run(host="0.0.0.0", port=80, debug=True)

