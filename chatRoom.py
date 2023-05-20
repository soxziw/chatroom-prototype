from glob import glob
from flask import Flask,request,redirect,render_template #新增代码。装入Flask

#用户模块，userMag，用户管理
import userTab
import ugTab
import friendsTab

webApp=Flask(__name__) #新增代码

#记录当前用户
curUserID = ""

#记录当前群聊
curGroup = ""


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

#!!!
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
    global curUserID,curGroup
    print(curUserID)
    print(curGroup)
    userName = userTab.getUser(curUserID).userName
    data=""
    # allGroup=chat.ChatUser(curUserID)
    # if curGroup!="":
    #     allData=chat.ChatGroup(curGroup)
    #     l=len(allData)
    #     data=data+"<div class=\"chatData\">"
    #     for n in range(0,l):
    #         data=data+f"{allData[n][0]}: {allData[n][1]}<br>"
    #     data=data+"</div>"+"""<form method="post" action="/sendAndReturn">
    #                             <p><input type="text" id="message" name="message" value="请输入" maxlength="150" class="message"/></p>
    #                             <p><input type="submit" value="发送"/></p>
    #                         </form>"""
    # return render_template("ChatRoom.html",userName=userName,group=groupSelectText(allGroup,curGroup),chatData=data)
    return render_template("ChatRoom.html",userName=userName,group="testGroup",chatData=data)

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