# chatroom-prototype
database midterm course project
实现的功能（每个功能对应前端一个函数/页面）：
1. 用户注册
2. 用户登录
3. 用户昵称修改
4. 申请好友
5. 接受好友
6. 发送私聊消息
7. 创建群聊
8. 加入群聊
9. 踢出群聊
10. 发送群聊消息
11. 搜索群用户消息
12. 搜索全局消息
13. （透明）显示全部好友
14. （透明）显示全部私聊消息
15. （透明）显示全部所在群聊
16. （透明）显示全部群聊成员
17. （透明）显示全部群聊消息
18. （透明）显示全部特定规则过滤后的消息

所有SQL均在下面方法中实现：
1. 用户表：userID(phone number) name password
   1. init() : void
   2. getUser(userID) : dict
   3. register(userID, name, password) : bool
   4. login(userID, password) : bool
   5. changeName(name, optUID) : bool
2. 群-用户表：userID groupID
   1. init() : void
   2. buildGroup(userID[], optUID) : bool
   3. addUser(groupID, userID, optUID) : bool
   4. deleteUser(groupID, userID, optUID) : bool
   5. getUID(groupID) : string
   6. getGID(optUID) : string
3. 群表：groupID(groupName_timestamp) groupName
   1. init() : void
   2. build(groupName) : string(groupID)
   3. changeName(groupID, optUID) : bool
4. 消息表：msgID(msg_timestamp) groupID userID msg
   1. init() : void
   2. writeMsg(groupID, msg, optUID) : bool
   3. getGMsg(groupID, optUID) : dict[]
   4. getGUMsg(groupID, userID, optUID) : dict[]
   5. getMsg(subMsg, optUID) : dict[]
5. 好友表：userID userID status
   1. init() : void
   2. apply(userID, optUID) : bool
   3. agree(userID, optUID) : bool
   4. getFriends(optUID) : dict[]