show databases

create database datarep;
use  datarep;

create table student ( id int NOT NULL auto_increment, 
firstname varchar(100), 
 age int(3), 
 PRIMARY KEY(id) );
 
 
 insert into student (firstname, age) values ('joe',56); 
 
 select * from student;
 update student set firstname=’mary’ where id = 1; 
 Delete from student where id = 1; 
 
 create table book ( id int NOT NULL auto_increment, 
title varchar(100), 
author varchar(100),
 price float(4), 
 PRIMARY KEY(id) );
 
  insert into book (title, author,price) values ('Data Analytics','Diarmuid WHELAN', 56.10); 
  insert into book (title, author,price) values ('Harry Potter','JK Rowling', 24.50);
    insert into book (title, author,price) values ('Python','Joe Bloggs', 99.99);
    select * from book;