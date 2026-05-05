--Part 1

--Part 1-1
SELECT e.FName, e.Minit, e.LName 
FROM employee e
where e.super_ssn = (SELECT ssn 
                    FROM EMPLOYEE
                    WHERE FName = 'Franklin'
                    AND Minit = 'T'
                    AND LName = 'Wong');
                    
-- Part 1-2
SELECT p.pname, p.pnumber, AVG(w.hours) AS Average_Hours
FROM project p
JOIN works_on w ON p.pnumber = w.pno
GROUP BY p.pname, p.pnumber;

-- Part 1-3
SELECT d.Dname, MAX(e.Salary) as Max_Salary
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname, d.dnumber
ORDER BY d.dnumber ASC;

-- Part 1-4
SELECT AVG(Salary) AS Female_Avg_Salary
FROM employee
WHERE sex='F';

--Part 1-5
SELECT d.dname as Department_Name, COUNT(e.ssn) as No_of_Employees
FROM department d
JOIN employee e ON d.dnumber = e.dno
GROUP BY d.dname, d.dnumber
HAVING AVG(e.salary) > 42000;

--Part 1-6
SELECT fname, minit, lname 
from employee 
where salary >= (SELECT MAX(salary) 
                   FROM employee) -27000;
                   
--Part 1-7-a
SELECT fname, minit, lname
FROM employee
WHERE SEX='F';

--Part 1-7-b
SELECT fname, minit, lname
FROM (SELECT * FROM employee WHERE sex='F') FemaleStaff;

--Part 1-8
SELECT fname, minit, lname
FROM employee
MINUS
SELECT e.fname, e.minit, e.lname
FROM employee e
JOIN works_on w on e.ssn = w.essn;

