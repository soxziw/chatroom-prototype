/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/5/5 11:44:19                            */
/*==============================================================*/


drop table if exists FRIENDS;

drop table if exists UG;

drop table if exists MESSAGE;

drop table if exists CHATGROUP;

drop table if exists USER;

/*==============================================================*/
/* Table: CHATGROUP                                             */
/*==============================================================*/
create table CHATGROUP
(
   groupID              int not null,
   groupName            varchar(20) not null,
   primary key (groupID)
);

/*==============================================================*/
/* Table: FRIENDS                                               */
/*==============================================================*/
create table FRIENDS
(
   userID               char(20) not null,
   friendID             char(20) not null,
   status               char(7) not null,
   primary key (userID, friendID)
);

/*==============================================================*/
/* Table: MESSAGE                                               */
/*==============================================================*/
create table MESSAGE
(
   msgID                int not null,
   userID               char(20) not null,
   groupID              int not null,
   msg                  longtext not null,
   primary key (msgID)
);

/*==============================================================*/
/* Table: UG                                                    */
/*==============================================================*/
create table UG
(
   userID               char(20) not null,
   groupID              int not null,
   status               char(7) not null,
   primary key (userID, groupID)
);

/*==============================================================*/
/* Table: USER                                                  */
/*==============================================================*/
create table USER
(
   userID               char(20) not null,
   name                 varchar(20) not null,
   password             varchar(20) not null,
   primary key (userID)
);

alter table FRIENDS add constraint FK_FRIENDS foreign key (userID)
      references USER (userID) on delete restrict on update restrict;

alter table FRIENDS add constraint FK_FRIENDS2 foreign key (friendID)
      references USER (userID) on delete restrict on update restrict;

alter table MESSAGE add constraint FK_GM foreign key (groupID)
      references CHATGROUP (groupID) on delete restrict on update restrict;

alter table MESSAGE add constraint FK_UM foreign key (userID)
      references USER (userID) on delete restrict on update restrict;

alter table UG add constraint FK_UG foreign key (userID)
      references USER (userID) on delete restrict on update restrict;

alter table UG add constraint FK_UG2 foreign key (groupID)
      references CHATGROUP (groupID) on delete restrict on update restrict;

