from glob import glob
from flask import Flask, request, redirect, render_template 
import groupDB, messageDB, userTab, ugTab, friendsTab

webApp = Flask(__name__) #新增代码

# 记录当前用户
curUserName = ""
curUserID = ""

# 记录当前群聊
curGroupName = ""
curGroupID = ""


@webApp.route("/") #新增代码，对应执行root()函数
def root():
    return redirect("/static/userLogin.html")

@webApp.route("/login",methods=('post',))
def login():
    userID = request.form["userID"]
    userPassword = request.form["userPassword"]
    checkState = userTab.login(userID, userPassword)

    if checkState == True: 
        global curUserID
        curUserID = userID
        print(curUserID)
    return checkState

@webApp.route("/register",methods=('post',))
def register():
    userID = request.form["userID"]
    userName = request.form["userName"]
    userPassword = request.form["userPassword"]
    checkState = userTab.register(userID, userName, userPassword)

    if checkState == True: 
        print(curUserID)
    return checkState

def groupSelectText(allGroup,curGroup): #生成群聊选择器
    l=len(allGroup)
    text=""
    for num in range(0,l):
        text=text+"<option value=\""+allGroup[num][0]+"\" "
        if allGroup[num][0]==curGroup:
            text=text+"selected"
        text=text+">"+allGroup[num][0]+"</option>"
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
def searchMsg():
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


@webApp.route("/changeName",methods=('post',))
def changeName():
    global curUserID
    if curUserID == "":
        return False
    userName = request.form["userName"]
    checkState = userTab.changeName(userName, curUserID)

    if checkState == True: 
        print(userName)
    return checkState

@webApp.route("/applyFriends",methods=('post',))
def applyFriends():
    global curUserID
    if curUserID == "":
        return False
    userID = request.form["userID"]
    checkState = friendsTab.apply(userID, curUserID)

    if checkState == True: 
        print(userID)
    return checkState

@webApp.route("/agreeFriends",methods=('post',))
def agreeFriends():
    userID = request.form["userID"]
    global curUserID
    if curUserID == "" or curUserID == userID:
        return False
    checkState = friendsTab.agree(userID, curUserID)

    if checkState == True: 
        print(userID)
    return checkState

@webApp.route("/friends")
def friends():
    global curUserID
    print(curUserID)
    allFriends = friendsTab.getFriends(curUserID)
    appData = f"<div class='chatData'>"
    for friend in allFriends:
        if friend.status == "UNSET":
            appData = appData + f"<div type='text' id='app_{friend.friendID}'>{friend.friendID}</div><button id='agree_{friend.friendID}'>同意</button><br>"
            appData = appData +"""<script type="text/javascript">
                                    $("#agree_""" + friend.friendID + """").click(function(){
                                        var userID = $("#app_""" + friend.friendID + """").val();
                                        $.post("/agreeFriends",{userID:userID},function(rtn){
                                            if (rtn) {
                                                alert("添加好友成功！");
                                                location.reload();
                                            } else {
                                                alert("添加好友失败！");
                                            }
                                        });
                                    });
                                </script>"""
    appData = appData + "</div>"
    userName = userTab.getUser(curUserID).userName
    return render_template("Friends.html",userName=userName,appData=appData)

if __name__=="__main__": #新增代码
    webApp.run(host="0.0.0.0",port=80,debug=True)

