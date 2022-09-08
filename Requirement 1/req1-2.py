#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv('accessPerDay.csv')
df


# In[2]:


df.info()


# In[3]:


list(df)


# # Q2a

# In[4]:


import sqlite3
import csv

conn = sqlite3.connect('students.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS submission_log')
cur.execute('CREATE TABLE submission_log (Name TEXT, "Group" TEXT, Date TEXT, Duration REAL)')
conn.commit()

rows = []
count = 0

with open('accessPerDay.csv') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)
    
    for row in csv_reader:
        rows.append(tuple(row))
        count += 1
        
cur.executemany('INSERT INTO submission_log (Name, "Group", Date, Duration) VALUES (?, ?, ?, ?)', rows)

conn.commit()
conn.close()


# In[5]:


conn = sqlite3.connect('students.db')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM submission_log')

assert count == cur.fetchone()[0] # Validate all rows are inserted

conn.close()


# # Q2b(i)

# In[6]:


conn = sqlite3.connect('students.db')
cur = conn.cursor()

cur.execute('SELECT "Group", AVG(Duration) FROM submission_log GROUP BY "Group" ORDER BY Duration DESC')

for record in cur.fetchall():
    print(f"{record[0]} - {record[1]}")
    
conn.close()


# # Q2b(ii)

# In[7]:


conn = sqlite3.connect('students.db')
cur = conn.cursor()

cur.execute('SELECT Name, SUM(Duration) FROM submission_log GROUP BY Name ORDER BY SUM(Duration) Desc')

print("Top 3 most active students")
for record in cur.fetchall()[:3]:
    print(f"{record[0]} - {record[1]}")


# In[8]:


cur.execute('SELECT Name, SUM(Duration) FROM submission_log GROUP BY Name ORDER BY SUM(Duration) Desc')

print("Top 3 least active students")
for record in cur.fetchall()[-3:]:
    print(f"{record[0]} - {record[1]}")
    
conn.close()

