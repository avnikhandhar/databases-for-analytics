import sqlite3

def setup_populate_db(file_path):

    # open the connection to DB
    conn = (sqlite3.connect('/Users/avnisanghvi/Desktop/courses/quarter-3/databases-for-analytics/week-3/hw-3/dsc450.db'))
    cursor = conn.cursor()

    # creating the tables
    cursor.execute("DROP TABLE IF EXISTS Employee_Jobs")
    cursor.execute("DROP TABLE IF EXISTS Employee_Location")
    cursor.execute("DROP TABLE IF EXISTS Job_Details")

    cursor.execute("""
        CREATE TABLE Employee_Jobs (
            First VARCHAR(15),
            Last VARCHAR(15),
            Job VARCHAR(15),

            CONSTRAINT Employee_Jobs_PK 
                PRIMARY KEY(First, Last, Job)
        )
    """)

    cursor.execute("""
        CREATE TABLE Job_Details (
            Job VARCHAR(15),
            Salary NUMBER(6,2),
            Assistant VARCHAR(30),

            CONSTRAINT Job_Details_PK 
                PRIMARY KEY(Job),

            CONSTRAINT Job_Details_FK1
                FOREIGN KEY(Job) 
                    REFERENCES Employee_Jobs(Job)
        )
    """)


    cursor.execute("""
        CREATE TABLE Employee_Location (
            First VARCHAR(15) ,
            Last VARCHAR(15) ,
            Address VARCHAR(80),
            
            CONSTRAINT Employee_Location_PK 
                PRIMARY KEY(First, Last), 
            
            CONSTRAINT Employee_Location_FK1 
                FOREIGN KEY(First) 
                    REFERENCES Employee_Job(First), 

            CONSTRAINT Employee_Location_FK2 
                FOREIGN KEY(Last) 
                    REFERENCES Employee_Job(Last) 
        )
    """)

    # populate the tables with data provided
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if not line.strip(): continue  # Skip empty lines

                # Split line by comma and strip whitespace
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 6: continue

                first, last, address, job, salary, assistant = parts

                # Data Cleaning: Convert 'NULL' strings to proper Python None (SQL NULL)
                # and convert salary to a float if it's not NULL
                salary_val = float(salary) if salary.upper() != 'NULL' else None
                assistant_val = assistant if assistant.upper() != 'NULL' else None
                address_val = address if address.upper() != 'NULL' else None

                cursor.execute("INSERT OR IGNORE INTO Employee_Location (First, Last, Address) VALUES (?, ?, ?)",
                               (first, last, address_val))

                cursor.execute("INSERT OR IGNORE INTO Job_Details (Job, Salary, Assistant) VALUES (?, ?, ?)",
                               (job, salary_val, assistant_val))

                cursor.execute("INSERT OR IGNORE INTO Employee_Jobs (First, Last, Job) VALUES (?, ?, ?)",
                               (first, last, job))

        conn.commit()
        print("Database populated successfully.\n")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # printing all the tables
    tables = ['Employee_Jobs', 'Employee_Location', 'Job_Details']

    for table in tables:
        print(f"Table: {table}-")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print()

    conn.close()

def verify_null():
    # open the connection to DB
    conn = (sqlite3.connect('/Users/avnisanghvi/Desktop/courses/quarter-3/databases-for-analytics/week-3/hw-3/dsc450.db'))
    cursor = conn.cursor()

    print('Finding all jobs with no salary specified using Salary IS NULL condition.')

    cursor.execute("SELECT * FROM Job_Details WHERE Salary IS NULL")
    result = cursor.fetchall()

    if not result:
        print("No row with NULL as a salary")
    else:
        print("Rows with NULL as a salary:")
        for row in result:
            print(row)

    conn.close()

# Function call to populate the tables
setup_populate_db('Data.txt')

# Function call to run the null verification
verify_null()