-- Part 1

-- Drop all the tables to clean up
DROP TABLE Animal;
-- ACategory: Animal category 'common', 'rare', 'exotic'.  May be NULL
-- TimeToFeed: Time it takes to feed the animal (hours)
CREATE TABLE Animal
(
  AID NUMBER(3, 0),
  AName VARCHAR2(35) NOT NULL,
  ACategory VARCHAR2(19),
  TimeToFeed NUMBER(4,2),  
  
  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);

INSERT INTO Animal VALUES(1, 'Galapagos Penguin', 'exotic', 0.5);
INSERT INTO Animal VALUES(2, 'Emperor Penguin', 'rare', 0.75);
INSERT INTO Animal VALUES(3, 'Sri Lankan sloth bear', 'exotic', 2.75);
INSERT INTO Animal VALUES(4, 'Grizzly bear', 'common', 3.0);
INSERT INTO Animal VALUES(5, 'Giant Panda bear', 'exotic', 1.5);
INSERT INTO Animal VALUES(6, 'Florida black bear', 'rare', 1.75);
INSERT INTO Animal VALUES(7, 'Siberian tiger', 'rare', 3.25);
INSERT INTO Animal VALUES(8, 'Bengal tiger', 'common', 2.75);
INSERT INTO Animal VALUES(9, 'South China tiger', 'exotic', 2.5);
INSERT INTO Animal VALUES(10, 'Alpaca', 'common', 0.75);
INSERT INTO Animal VALUES(11, 'Llama', NULL, 3.75);

-- Part 1-1 Find all the animals (their names) that take less than 1.75 hours to feed
SELECT aname FROM animal WHERE timetofeed < 1.75;

--Part 1-2 Find both the rare and exotic animals (in a single query, not two different queries)
SELECT aname,acategory FROM animal WHERE acategory IN ('exotic','rare');

--Part 1-3 Return the listings for all animals whose rarity is missing (NULL) in the database
SELECT aname FROM animal WHERE acategory is NULL;

--Part 1-4 Find the rarity rating of all animals that require between 1.3 and 2.7 hours to be fed
SELECT aname, acategory FROM animal WHERE timetofeed BETWEEN 1.3 and 2.7;

--Part 1-5 Find the minimum and maximum feeding time amongst all the animals in the zoo (in a single SQL query)
SELECT MIN(timetofeed) as MinTime , MAX(timetofeed) as MaxTime from animal;

--Part 1-6 Find the total (SUM) feeding time for all of the animals not related to a tiger
SELECT SUM(timetofeed) as totalTime FROM animal WHERE aname NOT LIKE '%tiger';

--Part 1-7 Find the average feeding time for all of the exotic animals
SELECT AVG(timetofeed) as AVG_EXOTIC from animal WHERE acategory='exotic';

--Part 1-8 Determine how many NULLs there are in the ACategory column using SQL
SELECT COUNT(*) as NULL_COUNT FROM animal WHERE acategory IS NULL;

--Part 1-9 Find all animals named 'Alpaca', 'Llama' or any other animals that are not listed as exotic
SELECT aname, acategory FROM animal WHERE aname IN ('Alpaca','Llama') OR acategory != 'exotic';