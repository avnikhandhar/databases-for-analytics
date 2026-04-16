
import sqlite3

conn = sqlite3.connect('dsc450.db')

import os
os.getcwd()

c = conn.cursor()

c.execute('CREATE TABLE DUMMY(A INTEGER, B INTEGER)')

conn.commit()
conn.close()

ST = '''CREATE TABLE Student
(
  ID VARCHAR(5),
  Name VARCHAR(25),
  Standing VARCHAR(8),  
  CONSTRAINT Student_PK
     PRIMARY KEY(ID)
); '''

c.execute(ST)

c.execute("INSERT INTO Student VALUES ('12345', 'Paul K', 'Grad');");

CT = """CREATE TABLE Course
(
          CourseID VARCHAR2(15),
          Name VARCHAR2(50),
          Credits INTEGER,
	CONSTRAINT Course_PK
	     PRIMARY KEY( CourseID)
); """

c.execute(CT)

c.execute("INSERT INTO Course VALUES ('CSC451', 'Database Design', 4);");

newData =[['23456', 'Larry P', 'Grad'],
		['34567', 'Ana B', 'Ugrad'],
		['45678', 'Mary Y', 'Grad'],
		['56789', 'Pat B', 'Ugrad']]

larry = newData[0]
larry
c.execute("INSERT INTO Student VALUES (?, ?, ?);", larry);

otherThreeStudents = newData[1:]
otherThreeStudents

c.executemany("INSERT INTO Student VALUES (?, ?, ?);", otherThreeStudents);












