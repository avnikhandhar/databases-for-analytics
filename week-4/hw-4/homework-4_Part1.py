import sqlite3

# drop all the tables to clean up
drop_handles = """
drop table if exists handles;
"""

drop_animal = """
drop table if exists animal;
"""

drop_zooKeeper = """
drop table if exists zookeeper;
"""

# create all the tables
create_zooKeeper = """
CREATE TABLE ZooKeeper
(
  ZID        NUMBER(3,0),
  ZName       VARCHAR2(25) NOT NULL,
  HourlyRate NUMBER(6, 2) NOT NULL,
  
  CONSTRAINT ZooKeeper_PK
     PRIMARY KEY(ZID)
);
"""

create_animal = """
CREATE TABLE Animal
(
  AID       NUMBER(3, 0),
  AName      VARCHAR(30) NOT NULL,
  ACategory VARCHAR(18),
  
  TimeToFeed NUMBER(4,2),  
  
  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);
"""

create_handles = """
CREATE TABLE Handles
(
  ZooKeepID      NUMBER(3,0),
  AnimalID     NUMBER(3,0),
  
  Assigned     DATE,
  
  CONSTRAINT Handles_PK
    PRIMARY KEY(ZooKeepID, AnimalID),
    
  CONSTRAINT Handles_FK1
    FOREIGN KEY(ZooKeepID)
      REFERENCES ZooKeeper(ZID),
      
  CONSTRAINT Handles_FK2
    FOREIGN KEY(AnimalID)
      REFERENCES Animal(AID)
);
"""

# inserting values into table
inserts = ["INSERT INTO ZooKeeper VALUES (1, 'Jim Carrey', 500);","INSERT INTO ZooKeeper VALUES (2, 'Tina Fey', 350);",
"INSERT INTO ZooKeeper VALUES (3, 'Rob Schneider', 250);",
"INSERT INTO Animal VALUES(1, 'Galapagos Penguin', 'exotic', 0.5);",
"INSERT INTO Animal VALUES(2, 'Emperor Penguin', 'rare', 0.75);",
"INSERT INTO Animal VALUES(3, 'Sri Lankan sloth bear', 'exotic', 2.5);",
"INSERT INTO Animal VALUES(4, 'Grizzly bear', 'common', 3.0);",
"INSERT INTO Animal VALUES(5, 'Giant Panda bear', 'exotic', 1.5);",
"INSERT INTO Animal VALUES(6, 'Florida black bear', 'rare', 1.75);",
"INSERT INTO Animal VALUES(7, 'Siberian tiger', 'rare', 3.5);",
"INSERT INTO Animal VALUES(8, 'Bengal tiger', 'common', 2.75);",
"INSERT INTO Animal VALUES(9, 'South China tiger', 'exotic', 2.25);",
"INSERT INTO Animal VALUES(10, 'Alpaca', 'common', 0.25);",
"INSERT INTO Animal VALUES(11, 'Llama', NULL, 3.5);",
"INSERT INTO Handles VALUES(1, 1, '01-Jan-2000');",
"INSERT INTO Handles VALUES(1, 2, '02-Jan-2000');",
"INSERT INTO Handles VALUES(1, 10, '01-Jan-2000');",
"INSERT INTO Handles VALUES(2, 3, '02-Jan-2000');",
"INSERT INTO Handles VALUES(2, 4, '04-Jan-2000');",
"INSERT INTO Handles VALUES(2, 5, '03-Jan-2000');",
"INSERT INTO Handles VALUES(3, 7, '01-Jan-2000');",
"INSERT INTO Handles VALUES(3, 8, '03-Jan-2000');",
"INSERT INTO Handles VALUES(3, 9, '05-Jan-2000');",
"INSERT INTO Handles Values(3, 10, '04-Jan-2000');"]

# Part 1-B

conn = (sqlite3.connect('/Users/avnisanghvi/Desktop/courses/quarter-3/databases-for-analytics/week-3/hw-3/dsc450.db')) # open the connection
cursor = conn.cursor()

# executing all the drops
cursor.execute(drop_handles)
cursor.execute(drop_animal)
cursor.execute(drop_zooKeeper)

# creating all the tables
cursor.execute(create_handles)
cursor.execute(create_animal)
cursor.execute(create_zooKeeper)

# inserting the rows
for ins in inserts:
    cursor.execute(ins)

# function to export data from tables to file
def export_data(table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    filename = f"{table_name.lower()}.txt"

    with open(filename, 'w') as f:
        for row in rows:
            piped_rows = '|'.join(map(str, row))
            f.write(piped_rows + '\n')

    print(f"Exported {table_name} to {filename}")

# listing all the tables
tables = ['ZooKeeper', 'Animal', 'Handles']

# call function of export for all tables
for table in tables:
    export_data(table)

# Part 1-C

f = open('animal.txt', 'r')
rows = f.readlines()

# 1-C-1
print("Names and Categories for animals related to a bear:")
for row in rows:
    columns = row.strip().split('|')
    name = columns[1]
    category = columns[2]

    if 'bear' in name.lower():
        print(f"Name: {name}, Category: {category}")

# 1-C-2
print("Names of animals related to a bear or a tiger and are common:")
for row in rows:
    columns = row.strip().split('|')
    name = columns[1]
    category = columns[2]

    if ('tiger' in name.lower() or 'bear' in name.lower()) and category == 'common':
        print(f"Name: {name}")

# 1-C-3
# animal id that have a handler
assigned_ids = set()

f2 = open('handles.txt', 'r')
rows2 = f2.readlines()

for row in rows2:
    h_cols = row.strip().split('|')
    assigned_ids.add(h_cols[1])

print("Animals with no assigned handler:")
# check for every animal in animal.txt file
for row in rows:
    columns = row.strip().split('|')
    animal_id = columns[0]
    animal_name = columns[1]

    if animal_id not in assigned_ids:
        print(f"Animal with no handler: {animal_name}")

# closing the file connection
f.close()
f2.close()

# closing the database connection
conn.commit()   # finalize inserted data
conn.close()    # close the connection