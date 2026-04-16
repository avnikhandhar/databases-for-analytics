
import sqlite3
conn = sqlite3.connect('dsc450.db')

c = conn.cursor()

result = c.execute('SELECT * FROM Student')

result.fetchone()
result.fetchall()

result.fetchall()

import os
os.getcwd()
os.chdir('/Users/fitsstudiouser/Desktop/Data')

fd = open('students.txt', 'r')

fd.read()
fd.seek(0)

oneLine = fd.readline()
oneLine
secondLine = fd.readline()
secondLine

allData = fd.readlines()

allData

for line in allData:
    print(line)

file = fd.read()

allDataLine = file.split('\n')

allDataLine = allDataLine[:-1]

example = '\t\tdata\n    \t  '

for line in allDataLine:
    values = line.split(', ')
    print(values)
    
    