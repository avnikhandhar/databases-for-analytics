
DROP TABLE Enrollment;
DROP TABLE Student;
DROP TABLE Course;
-- Course/Student Example

CREATE TABLE Student
(
  ID VARCHAR2(5),
  Name VARCHAR2(25) NOT NULL,
  Standing VARCHAR2(8),
  Age    NUMBER(3, 0);
  
  CONSTRAINT Student_PK
     PRIMARY KEY(ID)
);

CREATE TABLE Course
(
  CourseID VARCHAR2(15),
  Name VARCHAR2(50) UNIQUE,
  Credits NUMBER(*,0) CHECK (Credits > 0),
  
  CONSTRAINT Course_PK
     PRIMARY KEY( CourseID)
);

CREATE TABLE Enrollment
(
  StudentID VARCHAR2(5),
  CourseID VARCHAR2(15),
  Enrolled DATE,

  CONSTRAINT E_PK
     PRIMARY KEY(CourseID, StudentID),
  
  CONSTRAINT E_FK1
     FOREIGN KEY (CourseID)
       REFERENCES Course(CourseID),
       
  CONSTRAINT E_FK2
     FOREIGN KEY (StudentID)
       REFERENCES Student(ID)
);

INSERT INTO Course VALUES ('CSC211', 'Intro to Java I', 4);
INSERT INTO Course VALUES ('IT130', 'The Internet and the Web', 2);
INSERT INTO Course VALUES ('CSC452', 'Database Design', 4);

INSERT INTO Student VALUES ('12345', 'Paul K', 'Grad');
INSERT INTO Student VALUES ('23456', 'Larry P', 'Grad');
INSERT INTO Student VALUES ('34567', 'Ana B', 'Ugrad');
INSERT INTO Student VALUES ('45678', 'Mary Y', 'Grad');
INSERT INTO Student VALUES ('56789', 'Pat B', 'Ugrad');
INSERT INTO Student VALUES ('66789', 'Pat B', 'Grad');

INSERT INTO Enrollment VALUES('12345', 'CSC211', '01-Jan-2011');
INSERT INTO Enrollment VALUES('12345', 'CSC451', '02-Jan-2011');

INSERT INTO Enrollment VALUES('23456', 'IT130', '03-Jan-2011');

INSERT INTO Enrollment VALUES('34567', 'CSC211', '06-Jan-2011');
INSERT INTO Enrollment VALUES('34567', 'IT130', '07-Jan-2011');
INSERT INTO Enrollment VALUES('34567', 'CSC451', '11-Jan-2011');

INSERT INTO Enrollment VALUES('45678', 'IT130', '02-Jan-2011');
INSERT INTO Enrollment VALUES('45678', 'CSC211', '02-Jan-2011');


ALTER TABLE Student
  ADD CONSTRAINT CheckName
	  CHECK (Name IS NOT NULL);

ALTER TABLE STUDENT 
   ADD CONSTRAINT BadConstraint Unique(Name);

ALTER TABLE Student
  ADD CONSTRAINT AgeRange
  CHECK (Age BETWEEN 10 and 99);

ALTER TABLE Student
ADD CONSTRAINT FreshmenAge
Check (Standing = 'Freshman' AND Age < 30);

ALTER TABLE Student
		ADD Address VARCHAR2(15);

ALTER TABLE Student
	ADD (
		Income NUMBER(5, 2),
		 Taxes NUMBER(5)
	         );

ALTER TABLE Student
		DROP COLUMN Address;

ALTER TABLE Student
	  MODIFY Taxes NUMBER(5, 2);

ALTER TABLE Student
	  RENAME Column Taxes TO Tax;

INSERT INTO Enrollment 
  VALUES('45678', 'CSC451', 
          to_date('05/2013/7', 'mm/yyyy/dd'));

-- Store(StoreID, City, State)
-- Transaction(StoreID, TransID, Date, Amount)

-- get rid of existing tables
DROP TABLE Transaction;
DROP TABLE Store;

-- create the new tables, each with primary keys
CREATE TABLE Store(
        StoreID   NUMBER,
        City    VARCHAR2(20) NOT NULL,
        State  CHAR(2) NOT NULL,
      
      CONSTRAINT STORE_ID
            PRIMARY KEY (StoreID)
);

CREATE TABLE Transaction(
        StoreID   NUMBER,
	TransID  NUMBER,
	TDate       DATE,
        Amount  NUMBER(*, 2),

      CONSTRAINT DateCheck
           Check (TDate > To_Date('01-Jan-2010')),
      CONSTRAINT AmountCheck
           Check (Amount > 0.00),
      CONSTRAINT Transaction_ID
           PRIMARY KEY (StoreID, TransID),
      CONSTRAINT Transaction_FK1
           FOREIGN KEY (StoreID)
           REFERENCES Store(StoreID)
);

-- insert data...
INSERT INTO Store VALUES  (100, 'Chicago', 'IL');
INSERT INTO Store VALUES  (200, 'Chicago', 'IL');
INSERT INTO Store VALUES  
		(300, 'Schaumburg', 'IL');
INSERT INTO Store VALUES  (400, 'Boston', 'MA');
INSERT INTO Store VALUES  (500, 'Boston', 'MA');
INSERT INTO Store VALUES  
		(600, 'Portland', 'ME');


INSERT INTO Transaction Values(100, 1, '10-Oct-2011', 100.00);
INSERT INTO Transaction Values(100, 2, '11-Oct-2011', 120.00);
INSERT INTO Transaction Values(200, 1, '11-Oct-2011', 50.00);
INSERT INTO Transaction Values(200, 2, '11-Oct-2011', 70.00);
INSERT INTO Transaction Values(300, 1, '12-Oct-2011', 20.00);
INSERT INTO Transaction Values(400, 1, '10-Oct-2011', 10.00);

INSERT INTO Transaction Values(400, 2, '11-Oct-2011', 20.00);
INSERT INTO Transaction Values(400, 3, '12-Oct-2011', 30.00);
INSERT INTO Transaction Values(500, 1, '10-Oct-2011', 10.00);
INSERT INTO Transaction Values(500, 2, '10-Oct-2011', 110.00);
INSERT INTO Transaction Values(500, 3, '11-Oct-2011', 90.00);
INSERT INTO Transaction Values(600, 1, '11-Oct-2011', 300.00);


SELECT * FROM Store;

UPDATE Store SET city= 'Bohston'
    WHERE city = 'Boston';
SELECT * FROM Store WHERE city = 'Boston';

SELECT * FROM Transaction;
UPDATE Transaction SET TDate = NULL
    WHERE Amount <= 50;

UPDATE Store SET city = 'Bhoston'
    WHERE StoreID = 400;

UPDATE Store SET city= 'Boston'
    WHERE city LIKE 'B%ton';

SELECT * FROM Store WHERE city LIKE 'B___ton';

SELECT * FROM Transaction;
UPDATE Transaction SET Amount = Amount * 1.1;


DELETE FROM Store
        WHERE City = 'Boston';
SELECT * FROM Store WHERE City = 'Boston';

DELETE FROM Transaction
WHERE StoreID IN (400, 500);

SELECT * FROM Transaction
WHERE StoreID IN (400, 500);

DELETE FROM Store
        WHERE StoreID = 600;   

DELETE FROM Transaction
        WHERE TransID = 1;

DELETE FROM Transaction
        WHERE TDate <= to_date('11-Oct-2011');

DELETE FROM Transaction
        WHERE TDate != to_date('12-Oct-2011');   









ALTER TABLE Transaction
    ADD CONSTRAINT MaxTransactionAmt
    CHECK (Amount < 10000);

SELECT * FROM Transaction;
UPDATE Transaction SET Amount = -4 WHERE StoreID = 100;

ALTER TABLE Store
    ADD CONSTRAINT NoBostonStore
    CHECK (city != 'Boston');


ALTER TABLE Store
    ADD Manager VARCHAR2(50);
SELECT * FROM Store;

ALTER TABLE Store
    DROP COLUMN Manager;
    
ALTER TABLE Store
    ADD (Manager VARCHAR2(50),
         CallNumber VARCHAR2(12));

ALTER TABLE Store
     MODIFY Manager VARCHAR2(40);

ALTER TABLE Store
    DROP COLUMN StoreID;
     
ALTER TABLE Store
    RENAME Column CallNumber to CallNbr;
    
SELECT * FROM Store;





SELECT * FROM Store;
SELECT * FROM Transaction;

SELECT TDate, Amount 
FROM Transaction;

SELECT TDate, Amount
 FROM Transaction
 WHERE Amount >= 100;

SELECT * FROM Store
WHERE City LIKE 'B%ston';

SELECT * FROM Store
WHERE City LIKE 'B__st__';

SELECT DISTINCT city
 FROM store
 WHERE state = 'IL' OR state = 'ME';

 SELECT TDate, Amount
 FROM Transaction
 WHERE Amount > 40 AND Amount < 80;

SELECT *
 FROM Store
 WHERE (state = 'IL' OR city = 'Portland') AND StoreID != 100;

SELECT TDate, Amount
 FROM Transaction
  WHERE (Amount >=20 AND Amount <35)
      OR (Amount >100 AND Amount<= 120);

SELECT *
 FROM Store
 ORDER BY State, City;

  SELECT Amount, TDate, TransID
  FROM Transaction
  ORDER BY Amount;

 SELECT COUNT(DISTINCT State)
 FROM Store;

  SELECT SUM(Amount)
  FROM Transaction
  WHERE Amount <= 20 or Amount >= 100;


 SELECT TDate, Amount
 FROM Transaction
 WHERE Amount >=20
 ORDER BY TDate, Amount;

  SELECT AVG(Amount)
  FROM Transaction
  WHERE TDate = to_date('11-Oct-2011');

  SELECT MIN(Amount)
  FROM Transaction
  WHERE TDate = to_date('12-Oct-2011');


  SELECT MAX(Amount)
  FROM Transaction
  WHERE TDate = to_date('10-Oct-2011');

  SELECT MAX(Amount)
  FROM Transaction
  WHERE Amount < 55;

 SELECT state, COUNT(StoreID)
  FROM Store
  GROUP BY state;

  SELECT TDate, SUM(Amount)
  FROM Transaction
  GROUP BY TDate;

SELECT * 
FROM Store, Transaction;

SELECT * 
FROM Store, Transaction
WHERE Store.StoreID = Transaction.StoreID;



