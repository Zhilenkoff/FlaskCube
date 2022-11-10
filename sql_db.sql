create table if not exists mainmenu (
id integer primary key autoincrement,
title text not null,
url text not null
);
create table if not exists table1 (
id integer primary key autoincrement,
User text not null,
Post text not null,
Time text not null
);
--DROP TABLE table1;