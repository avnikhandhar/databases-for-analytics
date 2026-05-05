import sqlite3
import csv
import json

# Part 2

# connect to the db
conn = sqlite3.connect('chauffeurs_database.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS chauffeurs')
cursor.execute('''
CREATE TABLE IF NOT EXISTS chauffeurs (
    License_Number NUMBER(6,0),
    Renewed DATE,
    Status  VARCHAR2(10),
    Status_Date DATE,
    Driver_Type VARCHAR2(30),
    License_Type VARCHAR2(20),
    Original_Issue_Date DATE,
    Name VARCHAR2(100),
    Sex VARCHAR2(10),
    Chauffeur_City VARCHAR2(50),
    Chauffeur_State VARCHAR2(2),
    Record_Number VARCHAR2(20)
    )
''')

with open('Public_Chauffeurs_Short_hw3.csv', 'r', encoding='utf-8-sig') as fd:
    reader = csv.reader(fd)
    next(reader) # skip header row

    for row in reader:
        cleaned_row = []
        for i,val in enumerate(row):
            if val == 'NULL' or val == '' or val is None:
                cleaned_row.append(None)
            elif i == 0:
                cleaned_row.append(int(val))
            else:
                cleaned_row.append(val)

        cursor.execute('INSERT INTO chauffeurs values (?,?,?,?,?,?,?,?,?,?,?,?)', cleaned_row)

# commit the database
conn.commit()

# Part 2-a
cursor.execute('SELECT COUNT(*) FROM chauffeurs')
print(f"Total records: {cursor.fetchone()[0]}")

# Part 2-b
cursor.execute('SELECT COUNT(*) FROM chauffeurs WHERE Original_Issue_Date IS NULL')
print(f"Missing Issue Date: {cursor.fetchone()[0]}")

# close the connection to db
conn.close()

# Part 3

# connect to the db
conn = sqlite3.connect('chauffeurs_database.db')
cursor = conn.cursor()

# Part 3-a
cursor.execute('DROP TABLE IF EXISTS tweets')
cursor.execute('''
CREATE TABLE Tweets (
    created_at DATE,
    id_str NUMBER(30,0),
    text VARCHAR(150),
    source VARCHAR(150),
    in_reply_to_user_id VARCHAR(20),
    in_reply_to_screen_name VARCHAR(20),
    in_reply_to_status_id VARCHAR(20),
    retweet_count NUMBER(10,0),
    contributors VARCHAR(20)
)
''')

# Part 3-b
with open('Module5.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    tweet_list = content.split('EndOfTweet')

    for tweet_str in tweet_list:
        tweet_str = tweet_str.strip()
        if not tweet_str:
            continue

        try:
            tweet_data = json.loads(tweet_str)

            values = (
                tweet_data.get('created_at'),
                tweet_data.get('id_str'),
                tweet_data.get('text'),
                tweet_data.get('source'),
                tweet_data.get('in_reply_to_user_id'),
                tweet_data.get('in_reply_to_screen_name'),
                tweet_data.get('in_reply_to_status_id'),
                tweet_data.get('retweet_count'),
                tweet_data.get('contributors')
            )

            cursor.execute('''
                INSERT INTO tweets 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)

        except json.JSONDecodeError:
            # Handle potential formatting issues within the text file
            continue

conn.commit()

# Verification: Count total tweets loaded
cursor.execute('SELECT COUNT(*) FROM Tweets')
print(f"\nTotal Tweets loaded: {cursor.fetchone()[0]}")

conn.close()