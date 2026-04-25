# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:58:34 2026

@author: arasin
"""

Q1 = """
SELECT user_id, AVG(rating) AS AvgRating, COUNT(*)
FROM WatchHistory2
WHERE (rating >= 3 OR rating IS NULL) 
GROUP BY user_id
HAVING COUNT(*) >= 5
ORDER BY AvgRating"""

Q2 = """
SELECT user_id, AVG(rating), COUNT(*), COUNT(rating)
FROM WatchHistory2
GROUP BY user_id
HAVING AVG(rating) > (SELECT AVG(rating) FROM WatchHistory2)
ORDER BY user_id;"""

import sqlite3   # import cx_Oracle


fd = open('C:/Users/arasin/4_22_MovieDatabase.sql', 'r')
code = fd.read()
lines = code.split(';')

schema = []
load = []
cLoad = []
tables = []
for line in lines:
    if len(line)<=5:
        continue
    if 'INSERT INTO' in line:
        #load.append(line.strip())
        tbl = line.split()[2]  # Table name
        vals = line.split('VALUES')[1].strip()
        cLoad.append((tbl, vals[1:-1]))
    else:
        schema.append(line.strip())
        if 'CREATE TABLE' in line:
            tables.append(line.split('CREATE TABLE')[1].split()[0].strip())
        
#print(cLoad[:10])

conn = sqlite3.connect('dsc450_10.db') # open the connection
cursor = conn.cursor()

for line in schema:
    cursor.execute(line)

#for line in load:
#    cursor.execute(line)

for line in cLoad:  # Parametrized / clean load
    tbl = line[0]
    vals = list(line[1].split(', '))
    
    for i in range(len(vals)):
        if (len(vals[i])>5 and vals[i][0]=="'"):
            vals[i]=vals[i][1:-1]
        if (vals[i] == 'NULL'):
            vals[i] = None
    # Parametrized insert statement
    # INSERT INTO Table VALUES(?, ?, ?), ['A', 'B', 'C']
    #print( ' TABLE ' + tbl + " VALUES " + str(vals))
    qmarks = ['?'] * len(vals)
    ins = 'INSERT INTO ' + tbl + ' VALUES (' + ", ".join(qmarks) + ");"
    #print('INSERT '+ ins)
    #print(" VALUES " + str(vals))
    cursor.execute(ins, vals)

for table in tables:
    res = cursor.execute('SELECT COUNT(*) FROM '+ table)
    print(' TABLE '+ table + ' has ' + str(res.fetchall()[0][0]))

#res = cursor.execute(Q2).fetchall()
#for row in res:
#    print("  " + str(row))

conn.commit()   # finalize inserted data
conn.close()    # close the connection

fd.close()
