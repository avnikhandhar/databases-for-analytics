
import sqlite3
conn = sqlite3.connect('dsc450.db')
c = conn.cursor()

mike = ['83456', 'Mike P', 'Grad']

newRowInsert = "INSERT INTO Student VALUES ('%s', '%s', '%s');" 

insert = newRowInsert % tuple(mike)

insert

c.execute(insert)

mike2 = ['83452', 'Mike P 2nd', 'Grad']

c.execute("INSERT INTO Student VALUES (?, ?, ?);", mike2);

bobby = ['83456', "Robert'); DROP TABLE Studnts;", 'Grad']

insert = newRowInsert % tuple(bobby)

insert
