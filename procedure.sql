delimiter $$
drop procedure if exists REGISTER_USER $$
create procedure REGISTER_USER(
   in userID char(11), 
   in name varchar(20), 
   in password varchar(20)
)
begin
	insert ignore into USER(userID, name, password) values(userID, name, password);
end $$

drop procedure if exists UPDATE_USER $$
create procedure UPDATE_USER(
   in name varchar(20), 
   in userID char(11)
)
begin
	update USER set name = name where userID = userID;
end $$

drop procedure if exists INSERT_FRIEND $$
create procedure INSERT_FRIEND(
   in userID char(11),
   in friendID char(11),
   in status char(7)
)
begin
	insert ignore into FRIENDS(userID, friendID, status) values(userID, friendID, status);
end $$

drop procedure if exists UPDATE_FRIEND $$
create procedure UPDATE_FRIEND(
   in userID char(11),
   in friendID char(11),
   in status char(7)
)
begin
	update FRIENDS set status = status where (userID = userID and friendID = friendID);
end $$

drop procedure if exists ADD_USER_INTO_GROUP $$
create procedure ADD_USER_INTO_GROUP(
   in userID char(11),
   in groupID int,
   in status char(7)
)
begin
	insert into UG(userID, groupID, status) values(userID, groupID, status);
end $$

drop procedure if exists DELETE_USER_FROM_GROUP $$
create procedure DELETE_USER_FROM_GROUP(
   in userID char(11),
   in groupID int
)
begin
	delete from UG where userID = @userID and groupID = @groupID;
end $$
delimiter ;