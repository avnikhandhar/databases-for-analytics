SELECT * 
FROM Tickets
WhErE opened_date!=closed_date
AND UPPER(Category) = 'WIFI';

SELECT ticket_id, student_name, staff_name, priority
FROM tickets, students, staff
WHERE staff.staff_id = tickets.staff_id
AND students.student_id = tickets.student_id;


SELECT ticket_id, student_name, staff_name, priority
FROM (tickets FULL OUTER JOIN students ON students.student_id = tickets.student_id)
     LEFT OUTER JOIN  staff ON staff.staff_id = tickets.staff_id;
     
SELECT category, AVG(resolution_hours), COUNT(*)
FROM Tickets
GROUP BY category;

SELECT DISTINCT category
FROM Tickets;

SELECT student_name, COUNT(*)
FROM students, tickets
WHERE students.student_id = tickets.student_id
GROUP BY student_name
HAVING COUNT(*) >= 2;


SELECT Student_Name
FROM students, tickets
WHERE students.student_id = tickets.student_id
AND priority = 'Urgent';

SELECT Student_Name
FROM Students
WHERE EXISTS (SELECT *
              FROM Tickets
              WHERE priority = 'Urgent'
              AND students.student_id = tickets.student_id);


SELECT Student_Name
FROM Students
WHERE (SELECT COUNT(*)
              FROM Tickets
              WHERE priority = 'Urgent'
              AND students.student_id = tickets.student_id) >= 1;

SELECT student_name
FROM Students
WHERE Student_id IN
        (SELECT student_id
        FROM Tickets
        WHERE priority = 'Urgent');

SELECT ticket_id, category, resolution_hours, 
                   (SELECT AVG(resolution_hours)
                FROM Tickets)
FROM Tickets
WHERE resolution_hours >
                (SELECT AVG(resolution_hours)
                FROM Tickets);
                


SELECT ticket_id, category, resolution_hours, 
                   (SELECT AVG(resolution_hours)
                FROM Tickets tInner
                WHERE tOuter.category = tInner.category)
FROM Tickets tOuter
WHERE resolution_hours >
                (SELECT AVG(resolution_hours)
                FROM Tickets tInner
                WHERE tOuter.category = tInner.category);
                
                
SELECT ticket_id, category, resolution_hours
FROM Tickets
WHERE resolution_hours =
                (SELECT MAX(resolution_hours)
                FROM Tickets);


SELECT ticket_id, category, resolution_hours
FROM Tickets tOuter
WHERE resolution_hours =
                (SELECT MAX(resolution_hours)
                FROM Tickets tInner
                WHERE tOuter.category = tInner.category);


SELECT students.student_id, student_name
FROM Students, Tickets
WHERE students.student_id  = tickets.student_id
AND category = 'WiFi'

INTERSECT

SELECT students.student_id, student_name
FROM Students, Tickets
WHERE students.student_id  = tickets.student_id
AND category = 'Software';


SELECT students.student_id, student_name
FROM Students, Tickets
WHERE students.student_id  = tickets.student_id
AND category IN ('Software', 'WiFi')
GROUP BY students.student_id, student_name
HAVING COUNT(DISTINCT category) = 2;


SELECT student_id, student_name, COUNT(Major)
FROM Students
GROUP BY student_id, student_name


SELECT students.student_id, student_name
FROM Students, Tickets t1, Tickets t2
WHERE students.student_id  = t1.student_id AND
      students.student_id  = t2.student_id AND
      t1.category = 'WiFi' AND t2.category = 'Software';
      

SELECT *
FROM Students, Tickets t1, Tickets t2
WHERE students.student_id  = t1.student_id AND
      students.student_id  = t2.student_id AND
      t1.category = 'WiFi' AND t2.category = 'Software';
      
      
SELECT *
FROM Students, Tickets t1, Tickets t2
WHERE students.student_id  = t1.student_id AND
      students.student_id  = t2.student_id
ORDER BY students.student_id;



SELECT Tickets.student_id
FROM Tickets
WHERE category = 'WiFi'
UNION
SELECT Tickets.student_id
FROM Tickets
WHERE category = 'Printing'


SELECT * FROM Students
WHERE Student_id IN (SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'WiFi'
                     UNION
                     SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'Printing')


SELECT * FROM Students
WHERE Student_id IN (SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'WiFi'
INTERSECT
                     SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'Printing')


SELECT * FROM Students
WHERE Student_id IN (SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'WiFi'
MINUS  -- except
                     SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'Printing')

SELECT * FROM Students
WHERE Student_id NOT IN (SELECT Tickets.student_id
                     FROM Tickets
                     WHERE category = 'Software')
                     
SELECT * FROM Students
WHERE NOT EXISTS
                (SELECT *
                 FROM Tickets
                 WHERE category = 'Software' AND
                 students.student_id = tickets.student_id)


SELECT s.student_id, s.student_name, COUNT(t.ticket_id), AVG(t.resolution_hours)
FROM Students s, Tickets t
WHERE s.student_id = t.student_id
GROUP BY s.student_id, s.student_name;

CREATE VIEW StudentTicketSummary AS
SELECT s.student_id, s.student_name, 
       COUNT(t.ticket_id) AS NumTickets, AVG(t.resolution_hours) AS AvgResolveTime
FROM Students s, Tickets t
WHERE s.student_id = t.student_id
GROUP BY s.student_id, s.student_name;

SELECT *
FROM StudentTicketSummary;

SELECT Student_name
FROM StudentTicketSummary
    WHERE NumTickets = (SELECT MAX(NumTickets) FROM StudentTicketSummary);
    
SELECT SUM(NumTickets)
FROM StudentTicketSummary;
