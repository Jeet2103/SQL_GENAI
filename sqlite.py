import sqlite3

## Connect to sqlite

connection = sqlite3.connect("Student.db")

## Create a cursor object to insert record, create table
cursor = connection.cursor()

## Create a table
table_info = """
create table STUDENT_DATABASE(NAME VARCHAR(25),
 CLASS VARCHAR(25), SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

## Insert some more records

cursor.execute('''Insert Into STUDENT_DATABASE values('Jeet Nandigrami','AIML','A',100)''')
cursor.execute('''Insert Into STUDENT_DATABASE values('Soumyajit Dutta','AIML','B',99)''')
cursor.execute('''Insert Into STUDENT_DATABASE values('Adreeja Mahato','AEIE','A',100)''')
cursor.execute('''Insert Into STUDENT_DATABASE values('Debaditya Ghosh','AIML','A',98)''')
cursor.execute('''Insert Into STUDENT_DATABASE values('Dyuti Dasgupta','Bio tech','D',001)''')
cursor.execute('''Insert Into STUDENT_DATABASE values('Pratyush Palit','DS','A',97)''')

## Display the record

print("The Inserted recoreds are : ")
data = cursor.execute('''Select * from STUDENT_DATABASE''')
for row in data:
    print(row)

## Commit changes in database
connection.commit()
connection.close()