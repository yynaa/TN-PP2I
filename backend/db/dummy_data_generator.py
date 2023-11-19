import sqlite3
import random

connexion = sqlite3.connect('backend/db/dummy.db')
cursor = connexion.cursor()

db_path = 'backend/db/dummy.db'

# CREATING ALL THE TABLE IN THE DB
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buildings
        ([building_id] INTEGER PRIMARY KEY NOT NULL, [building_name] VARCHAR, [address] VARCHAR, [GPS_lat] REAL, [GPS_long] REAL, [evaluation] INTEGER)          
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
        ([login] VARCHAR, [email] VARCHAR, [password] VARCHAR, [display_name] VARCHAR, [creation_date] DATE, PRIMARY KEY ([login],[email]))
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reviews
        ([review_id] INTEGER PRIMARY KEY NOT NULL, [user_login] VARCHAR, [content] VARCHAR)
    ''')

for i in range(100):
    cursor.execute('''INSERT INTO Buildings VALUES (?, ?, ?, ?, ?, ?)''', (i, "Building " + str(i), "Address " + str(i), 48.689 + random.uniform(-1,1), 6.2 + random.uniform(-1,1), 5))

connexion.close()