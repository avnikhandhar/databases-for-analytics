import sqlite3
import random
import time
from collections import defaultdict

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
        SELECT s.StudentID, s.Name, s.GradYear, g.CName, g.CGrade, g.Date_grades, c.Department, c.Credits
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
        f"{'101':<15} | {'New Student A':<15} | {'2026':<15} | {'Intro to Python':<15} | {'3.5':<15} | {'2026-01-01':<15} | {'History':<15} | {'4':<15}\n",
        f"{'102':<15} | {'New Student B':<15} | {'2026':<15} | {'Intro to Python':<15} | {'3.2':<15} | {'2026-01-01':<15} | {'Biology':<15} | {'4':<15}\n",
        f"{'103':<15} | {'New Student C':<15} | {'2026':<15} | {'Machine Learning':<15} | {'4.0':<15} | {'2026-01-01':<15} | {'Art':<15} | {'4':<15}\n",

        # Violation 2: {CName, StudentID} -> Different Grades (1.0 vs 2.5 for Student 98)
        f"{'98':<15} | {'Jennifer J':<15} | {'2027':<15} | {'Database Systems':<15} | {'1.0':<15} | {'2026-01-01':<15} | {'CS':<15} | {'4':<15}\n",
        f"{'98':<15} | {'Jennifer J':<15} | {'2027':<15} | {'Database Systems':<15} | {'2.5':<15} | {'2026-01-01':<15} | {'CS':<15} | {'4':<15}\n",
        f"{'99':<15} | {'Jennifer B':<15} | {'2025':<15} | {'Machine Learning':<15} | {'0.0':<15} | {'2026-01-01':<15} | {'CS':<15} | {'4':<15}\n"
    ]

    with open(file_path, "a") as f:
        f.writelines(violations)
    print(f"Successfully added 6 violation rows.")


# Part 4
def detect_fd_violations(file_path="university_data_denormalized.txt"):
    data = []
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            # Skip header and separator line
            for line in lines[2:]:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 8:
                    data.append({
                        'StudentID': parts[0],
                        'CName':     parts[3],
                        'CGrade':    parts[4],
                        'Department':parts[6]
                    })
    except FileNotFoundError: return

    # Check FD: CName -> Department
    cname_dept_map = defaultdict(set)
    print("\n--- Checking FD: CName -> Department ---")
    for row in data:
        if row['CName'].lower() != 'none':
            cname_dept_map[row['CName']].add(row['Department'])

    for cname, depts in cname_dept_map.items():
        if len(depts) > 1:
            print(f"VIOLATION: Course '{cname}' associated with multiple departments: {depts}")

    # Check FD: {CName, StudentID} -> CGrade
    composite_grade_map = defaultdict(set)
    print("\n--- Checking FD: {CName, StudentID} -> CGrade ---")
    for row in data:
        if row['CName'].lower() != 'none':
            key = (row['CName'], row['StudentID'])
            composite_grade_map[key].add(row['CGrade'])

    for (cname, sid), grades in composite_grade_map.items():
        if len(grades) > 1:
            print(f"VIOLATION: Student {sid} in '{cname}' has multiple grades: {grades}")

# Part 5
def load_txt_to_sqlite(txt_file="university_data_denormalized.txt", db_name="university_flat.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS FlatUniversity")
    cursor.execute("""
        CREATE TABLE FlatUniversity (
            RowID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID TEXT, Name TEXT, GradYear TEXT, 
            CName TEXT, CGrade TEXT, Date_grades TEXT, 
            Department TEXT, Credits TEXT
        )
    """)
    with open(txt_file, "r") as f:
        lines = f.readlines()[2:]
        for line in lines:
            parts = [None if p.strip().upper() in ["NULL", "NONE"] else p.strip() for p in line.split("|")]
            if len(parts) == 8:
                cursor.execute("INSERT INTO FlatUniversity (StudentID, Name, GradYear, CName, CGrade, Date_grades, Department, Credits) VALUES (?,?,?,?,?,?,?,?)", parts)
    conn.commit()
    conn.close()

# Part 5.a and 5.b
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

# Part 6.a
def query_original_tables(db_name="university.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = """
    SELECT g.Date_grades, MAX(c.Credits), AVG(c.Credits), MIN(s.GradYear)
    FROM Grade g
    JOIN Course c ON g.CName = c.CName
    JOIN Student s ON g.StudentID = s.StudentID
    GROUP BY g.Date_grades;
    """

    start_time = time.perf_counter()
    cursor.execute(query)
    results = cursor.fetchall()
    end_time = time.perf_counter()

    conn.close()
    print(f"Original SQL Execution Time: {end_time - start_time:.6f} seconds")
    return results

# Part 6.b
def query_qx_using_view(db_name="university.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Define Query
    query_qx = """
    SELECT 
        Date_grades, 
        MAX(Credits), 
        AVG(Credits), 
        MIN(GradYear)
    FROM StudentEnrollmentView
    WHERE Date_grades IS NOT NULL  -- Exclude non-enrolled students (NULL dates)
    GROUP BY Date_grades;
    """

    # Time the execution
    start_time = time.perf_counter()
    cursor.execute(query_qx)
    results = cursor.fetchall()
    end_time = time.perf_counter()

    # Display Results
    print(f"View-Based SQL Execution Time: {end_time - start_time:.6f} seconds")
    print("-" * 60)
    print(f"{'Date':<12} | {'Max Credits':<12} | {'Avg Credits':<12} | {'Min GradYear':<12}")
    print("-" * 60)
    for row in results[:5]:  # Display first 5 for brevity
        date, max_c, avg_c, min_g = row
        print(f"{str(date):<12} | {max_c:<12} | {avg_c:<12.2f} | {min_g:<12}")

    conn.close()
    return results

# Part 6.c
def query_qx_with_python(file_path="university_data_denormalized.txt"):
    data_groups = defaultdict(lambda: {'credits': [], 'grad_years': []})
    start_time = time.perf_counter()

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

            for line in lines[2:]:
                parts = [p.strip() for p in line.split("|")]

                if len(parts) >= 7:
                    date = parts[4]
                    credits_str = parts[5]
                    grad_year_str = parts[6]

                    # Skip non-enrolled students and header/footer noise
                    if date.lower() not in ['none', 'null', 'date_grades']:
                        try:
                            # Safely convert to numeric types
                            data_groups[date]['credits'].append(float(credits_str))
                            data_groups[date]['grad_years'].append(int(grad_year_str))
                        except ValueError:
                            # This skips rows where the data isn't a number
                            continue

        # Aggregation Logic
        results = []
        for date in sorted(data_groups.keys()):
            creds = data_groups[date]['credits']
            years = data_groups[date]['grad_years']
            if creds:
                results.append((date, max(creds), sum(creds) / len(creds), min(years)))

        end_time = time.perf_counter()
        print(f"6.c Python TXT Execution Time: {end_time - start_time:.6f} seconds")
        return results

    except FileNotFoundError:
        print("File not found. Please ensure Part 2 export ran successfully.")

if __name__ == "__main__":
    create_and_populate_db() # creation of DB
    update_and_verify()  # Part 1
    export_view_to_txt()  # Part 2
    add_fd_violations()   # Part 3
    detect_fd_violations() # Part 4
    load_txt_to_sqlite()   # Part 5
    verify_violations_sql() # Part 5a and 5b
    original_results = query_original_tables() # Part 6.a
    print(original_results)
    query_qx_using_view() # Part 6.b
    query_qx_with_python() # Part 6.c

    # Part 6.d
    '''
    The three outputs from 6.a, 6.b and 6.c are same but with a difference of time it took to execute. The output
    matched because the functional dependencies are preserved. It is observed that querying the original table is the
    fastest method and the extraction by view is slower than the querying of original table. While, the method which
    used Python seems okay here, but once the data is increased, the time will also increase accordingly because it
    is linearly parsing the text, making it slower with more data.
    '''