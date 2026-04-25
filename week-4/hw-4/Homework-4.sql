-- Part 1-A

-- Part 1-A-1
SELECT ANAME, timetofeed
FROM ANIMAL
WHERE acategory='rare'
ORDER BY timetofeed;

-- Part 1-A-2
SELECT aname, acategory
FROM animal
WHERE aname LIKE '%tiger%';

-- Part 1-A-3
SELECT aname
from animal
WHERE aname like '%bear%' AND acategory != 'common';

-- Part 1-A-4
SELECT aname
FROM animal
WHERE aname NOT LIKE '%bear%';

-- Part 1-A-5
SELECT a.aname as Animal_Name , h.zookeepid as Zoo_Keeper_ID
FROM animal a
join handles h on a.aid = h.animalid;

-- Part 1-A-6
SELECT a.aname as Animal_Name , h.zookeepid as Zoo_Keeper_ID
FROM animal a
left join handles h on a.aid = h.animalid;

-- Part 1-A-7
SELECT z.zname as zoo_keeper, MIN(a.timetofeed) as MinFeedingTime
FROM zookeeper z
LEFT JOIN handles h on z.zid = h.zookeepid
LEFT JOIN animal a on h.animalid = a.aid
group by z.zname;

-- Part 1-A-8
SELECT TO_CHAR(h.assigned, 'DD-Mon-YYYY') as Assignment_Date, z.zname as zoo_Keeper_name, a.aname as Animal_Name
FROM zookeeper z
JOIN handles h on z.zid = h.zookeepid
JOIN animal a on h.animalid = a.aid
ORDER BY h.assigned;