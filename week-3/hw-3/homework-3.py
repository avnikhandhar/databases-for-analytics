import sqlite3

# Part 2-a

# I have executed the .py file provided to us.

conn = sqlite3.connect('dsc450.db') # open the connection
cursor = conn.cursor()

# selecting all data from 'animal' table
cursor.execute('select * from animal')
rows = cursor.fetchall()

# open a file to write the rows
f = open('animal.txt', 'w')

for row in rows:
    str_row = [str(item) for item in row] # row is a tuple so changing it to a string
    line = ','.join(str_row) #joining the row items with a comma
    f.write(line + "\n") # write to the file with new line at the end for next row

f.close() # close the file

conn.commit() # close the connection
conn.close()

print("Data exported to animal.txt")

# Part 2-b

# connecting to a new database
conn2 = sqlite3.connect('dsc450_reloaded.db')
cursor2 = conn2.cursor()

# create table 'animal' structure
createtbl = """
CREATE TABLE Animal
(
  AID       NUMBER(3, 0),
  AName      VARCHAR2(30) NOT NULL,
  ACategory VARCHAR2(18),

  TimeToFeed NUMBER(4,2),

  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);
"""
cursor2.execute(createtbl)

# reading the file into list of tuples
animal_list = []

fd = open('animal.txt', 'r') # open the .txt file in read mode

for line in fd:
    parts = line.strip().split(',') # removing the \n from end and splitting by ','

    aid = int(parts[0])
    name = parts[1].strip()
    category = parts[2].strip() if parts[2].strip() != "" else None
    time = float(parts[3])

    animal_list.append((aid, name, category, time))

fd.close() # file closed

# loading data into table
insert = "INSERT INTO animal VALUES (?, ?, ?, ?)"
cursor2.executemany(insert, animal_list)

conn2.commit() # save the insertion

# verify the insertion
cursor2.execute("SELECT COUNT(*) FROM animal")
row_count = cursor2.fetchone()[0]

print(f"{row_count} rows inserted into the table")

conn2.close() # close the connection