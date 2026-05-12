import sqlite3
import random

def create_and_populate_db(db_name="university.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Schema

    # drop all the tables to clean up
    drop_student = """
    drop table if exists Student;
    """

    drop_course = """
    drop table if exists course;
    """

    drop_grade = """
    drop table if exists grade;
    """

    # Student Schema
    create_student = """
    CREATE TABLE IF NOT EXISTS Student(
        StudentID NUMBER(6,0),
        Name VARCHAR2(50),
        Address VARCHAR2(50),
        GradYear NUMBER(4,0),
        
        CONSTRAINT Student_PK
        PRIMARY KEY(StudentID)
    );
    """

    # Course Schema
    create_course = """
    CREATE TABLE IF NOT EXISTS Course (
            CName VARCHAR2(15),
            Department VARCHAR2(20),
            Credits NUMBER(2,0),

            CONSTRAINT Course_PK
            PRIMARY KEY(CName)
        );
    """

    # Grade Schema
    create_grade = """
    CREATE TABLE IF NOT EXISTS Grade (
            CName VARCHAR2(15),
            StudentID NUMBER(6,0),
            Date_grades Date,
            CGrade INTEGER,
            
            CONSTRAINT Grade_PK
            PRIMARY KEY(CName,StudentID),
            
            CONSTRAINT Grade_FK1
            FOREIGN KEY(CName)
            REFERENCES Course(CName),
            
            CONSTRAINT Grade_FK2
            FOREIGN KEY(StudentID)
            REFERENCES Student(StudentID)
        );
    """
    cursor.execute(drop_student)
    cursor.execute(drop_course)
    cursor.execute(drop_grade)

    cursor.execute(create_student)
    cursor.execute(create_course)
    cursor.execute(create_grade)

    # Populate Courses
    departments = ['CS', 'Data Science', 'Math', 'Physics', 'History']
    course_names = [
        "Intro to Python", "Machine Learning", "Database Systems",
        "Linear Algebra", "Calculus I", "Quantum Physics",
        "World History", "AI Agents", "Natural Language Processing",
        "Data Visualization", "Ethics in Tech", "Discrete Math"
    ]

    for name in course_names:
        cursor.execute("INSERT INTO Course VALUES (?, ?, ?)",
                       (name, random.choice(departments), random.randint(3, 4)))

    # Populate Students
    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

    for i in range(1, 101):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        address = f"{random.randint(100, 999)} University Ave"
        grad_year = random.randint(2025, 2028)
        cursor.execute("INSERT INTO Student VALUES (?, ?, ?, ?)", (i, name, address, grad_year))

    # Generate Enrollments
    active_students = list(range(1, 98))
    active_courses = course_names[:-2]

    enrollments = set()
    student_course_counts = {sid: 0 for sid in active_students}

    while len(enrollments) < 220:
        s_id = random.choice(active_students)
        c_name = random.choice(active_courses)

        # Check constraints: Not already enrolled and hasn't exceeded 3 courses
        if (c_name, s_id) not in enrollments and student_course_counts[s_id] < 3:
            enrollments.add((c_name, s_id))
            student_course_counts[s_id] += 1

            date = f"2026-0{random.randint(1, 5)}-{random.randint(10, 28)}"
            grade = round(random.uniform(2.0, 4.0), 1)
            cursor.execute("INSERT INTO Grade VALUES (?, ?, ?, ?)", (c_name, s_id, date, grade))

    conn.commit()
    print(f"Database '{db_name}' created and populated successfully.")

    # Verification queries
    cursor.execute("SELECT COUNT(*) FROM Student")
    print(f"Total Students: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM Course")
    print(f"Total Courses: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM Grade")
    print(f"Total Enrollments: {cursor.fetchone()[0]}")

    conn.close()

# Part 1
def update_and_verify(db_name="university.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the view
    cursor.execute("DROP VIEW IF EXISTS StudentEnrollmentView")
    cursor.execute("""
        CREATE VIEW StudentEnrollmentView AS
        SELECT s.StudentID, s.Name, g.CName, g.CGrade, c.Department
        FROM Student s
        LEFT JOIN Grade g ON s.StudentID = g.StudentID
        LEFT JOIN Course c ON g.CName = c.CName
    """)

    # Count records before insertion
    cursor.execute("SELECT COUNT(*) FROM StudentEnrollmentView")
    count_before = cursor.fetchone()[0]
    print(f"Record count in view BEFORE insertion: {count_before}")

    # Enroll 5 more students
    new_enrollments = [
        ('Intro to Python', 98, '2026-05-12', 3.8),
        ('Machine Learning', 99, '2026-05-12', 4.0),
        ('Database Systems', 100, '2026-05-12', 3.5),
        ('Linear Algebra', 98, '2026-05-12', 3.7),
        ('Calculus I', 99, '2026-05-12', 3.9)
    ]

    print("Inserting 5 new enrollment records...")
    cursor.executemany("INSERT INTO Grade VALUES (?, ?, ?, ?)", new_enrollments)
    conn.commit()

    # Count records after insertion
    cursor.execute("SELECT COUNT(*) FROM StudentEnrollmentView")
    count_after = cursor.fetchone()[0]
    print(f"Record count in view AFTER insertion: {count_after}")

    # Validation:
    cursor.execute("""
        SELECT StudentID, Name, CName 
        FROM StudentEnrollmentView 
        WHERE StudentID IN (98, 99, 100)
    """)
    for row in cursor.fetchall():
        print(row)

    conn.close()

# Part 2
def export_view_to_txt(db_name="university.db", output_file="university_data_denormalized.txt"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query the view created in the previous step
    cursor.execute("SELECT * FROM StudentEnrollmentView")
    rows = cursor.fetchall()

    # Get column names for the header
    colnames = [description[0] for description in cursor.description]

    with open(output_file, "w") as f:
        header = " | ".join(f"{col:<15}" for col in colnames)
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")

        for row in rows:
            formatted_row = " | ".join(f"{str(val):<15}" for val in row)
            f.write(formatted_row + "\n")

    conn.close()
    print(f"Data successfully exported to {output_file}")

# Part 3
def add_fd_violations(file_path="university_data_denormalized.txt"):
    violations = [
        # Violation : CName -> Department
        f"{'101':<15} | {'New Student A':<15} | {'Intro to Python':<15} | {'3.5':<15} | {'History':<15}\n",
        f"{'102':<15} | {'New Student B':<15} | {'Intro to Python':<15} | {'3.2':<15} | {'Biology':<15}\n",
        f"{'103':<15} | {'New Student C':<15} | {'Machine Learning':<15} | {'4.0':<15} | {'Art':<15}\n",

        # Violation : {CName, StudentID} -> CGrade
        f"{'98':<15} | {'Patricia Smith':<15} | {'Intro to Python':<15} | {'1.0':<15} | {'CS':<15}\n",
        f"{'98':<15} | {'Patricia Smith':<15} | {'Intro to Python':<15} | {'2.5':<15} | {'CS':<15}\n",
        f"{'99':<15} | {'Linda Garcia':<15} | {'Machine Learning':<15} | {'0.0':<15} | {'CS':<15}\n"
    ]

    try:
        with open(file_path, "a") as f:
            f.writelines(violations)
        print(f"Successfully added 6 violation rows to {file_path}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please run Part 2 first.")

# Part 4
def detect_fd_violations(file_path="university_data_denormalized.txt"):
    data = []

    # Read and parse the file
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines[2:]:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5:
                    data.append({
                        'StudentID': parts[0],
                        'Name': parts[1],
                        'CName': parts[2],
                        'CGrade': parts[3],
                        'Department': parts[4]
                    })
    except FileNotFoundError:
        print("File not found.")
        return

    # Check CName -> Department
    cname_dept_map = {}
    print(" Checking FD: CName -> Department ")
    for row in data:
        cname = row['CName']
        dept = row['Department']

        if cname not in cname_dept_map:
            cname_dept_map[cname] = set()
        cname_dept_map[cname].add(dept)

    violations_found = False
    for cname, depts in cname_dept_map.items():
        if len(depts) > 1:
            print(f"VIOLATION: Course '{cname}' maps to multiple departments: {depts}")
            violations_found = True
    if not violations_found: print("No violations found.")

    # Check {CName, StudentID} -> CGrade
    composite_grade_map = {}
    print("\n Checking FD: {CName, StudentID} -> CGrade")
    violations_found = False
    for row in data:
        key = (row['CName'], row['StudentID'])
        grade = row['CGrade']

        if key not in composite_grade_map:
            composite_grade_map[key] = set()
        composite_grade_map[key].add(grade)

    for (cname, sid), grades in composite_grade_map.items():
        if len(grades) > 1:
            print(f"VIOLATION: Student {sid} in '{cname}' has multiple grades: {grades}")
            violations_found = True
    if not violations_found: print("No violations found.")

# Part 5
def load_txt_to_sqlite(txt_file="university_data_denormalized.txt", db_name="university_flat.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a single flat table
    cursor.execute("DROP TABLE IF EXISTS FlatUniversity")
    cursor.execute("""
        CREATE TABLE FlatUniversity (
            RowID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID TEXT,
            Name TEXT,
            CName TEXT,
            CGrade TEXT,
            Department TEXT
        )
    """)

    # Load data from TXT
    with open(txt_file, "r") as f:
        lines = f.readlines()[2:]  # Skip header and separator
        for line in lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 5:
                # Replace 'NULL' or 'None' strings with actual None (SQL NULL)
                cleaned_parts = [None if p.upper() in ["NULL", "NONE"] else p for p in parts]
                cursor.execute("""
                    INSERT INTO FlatUniversity (StudentID, Name, CName, CGrade, Department) 
                    VALUES (?, ?, ?, ?, ?)
                """, cleaned_parts)

    conn.commit()
    print(f"Loaded data into table 'FlatUniversity' in {db_name}")
    conn.close()

# Part 5a and 5b
def verify_violations_sql(db_name="university_flat.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    print("SQL Detection: CName -> Department")
    cursor.execute("""
        SELECT CName, GROUP_CONCAT(DISTINCT Department)
        FROM FlatUniversity
        WHERE CName IS NOT NULL
        GROUP BY CName
        HAVING COUNT(DISTINCT Department) > 1
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Violation: Course '{row[0]}' is associated with departments: {row[1]}")

    print("\n SQL Detection: {CName, StudentID} -> CGrade")
    cursor.execute("""
        SELECT StudentID, CName, GROUP_CONCAT(DISTINCT CGrade)
        FROM FlatUniversity
        WHERE CName IS NOT NULL
        GROUP BY StudentID, CName
        HAVING COUNT(DISTINCT CGrade) > 1
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Violation: Student {row[0]} in course '{row[1]}' has grades: {row[2]}")

    conn.close()

if __name__ == "__main__":
    create_and_populate_db() # creation of DB
    update_and_verify()  # Part 1
    export_view_to_txt()  # Part 2
    add_fd_violations()   # Part 3
    detect_fd_violations() # Part 4
    load_txt_to_sqlite()   # Part 5
    verify_violations_sql() # Part 5a and 5b