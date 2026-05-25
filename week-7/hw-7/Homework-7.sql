-- Part 3.a

CREATE OR REPLACE TRIGGER Cap_Course_Number
BEFORE INSERT OR UPDATE OF CourseNr ON course
FOR EACH ROW
BEGIN
    -- Convert the string to a number for comparison
    IF TO_NUMBER(:NEW.CourseNr) >= 598 THEN
        :NEW.CourseNr := '597';
    END IF;
EXCEPTION
    WHEN VALUE_ERROR THEN
        NULL; 
END;
/

-- Validation of the trigger created

-- View current data before tests
SELECT CID, CourseName, CourseNr FROM course;

-- Insert a normal course below 597
INSERT INTO course VALUES (5001, 'Advanced Database Systems', 'CSC', '452');

-- Insert a course higher than 597
INSERT INTO course VALUES (5002, 'Independent Research Study', 'CSC', '601');

-- Insert a boundary course at exactly 598
INSERT INTO course VALUES (5003, 'Special Topics in IT', 'IT', '598');

-- Verify the insertions
SELECT CID, CourseName, CourseNr FROM course WHERE CID IN (5001, 5002, 5003);


-- Update an existing valid course to a value above 597 
UPDATE course 
SET CourseNr = '750' 
WHERE CID = 1020; 

-- Update an existing valid course to a legal value below 597 
UPDATE course 
SET CourseNr = '350' 
WHERE CID = 1092;

-- Verify the updates
SELECT CID, CourseName, CourseNr FROM course WHERE CID IN (1020, 1092);