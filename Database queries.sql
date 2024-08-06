--Table creation
CREATE table characters (cid integer PRIMARY key AUTOINCREMENT, cname text NOT NULL);
CREATE table groups (gid integer PRIMARY KEY autoincrement, gname text NOT NULL);
CREATE table cgrelations (characterid integer , groupid integer ,FOREIGN KEY (characterid) REFERENCES characters(cid),FOREIGN KEY (groupid) REFERENCES groups(gid));
create table media (did integer primary key autoincrement,dname text not null);
--Add values
INSERT INTO characters (name) values ('Yuval');
INSERT INTO groups (name) values ('Red team');
INSERT INTO media (name) values ('life is strange');
INSERT INTO cgrelations (characterid,groupid) values (1,1);
--Search command
select * from characters;
SELECT characterid from cgrelations where groupid=1; --find the characters in a groups
SELECT groupid from cgrelations where characterid=1; --find the groups a character is in
SELECT * from characters where cname like 'Yuv%'; --SearchTab 