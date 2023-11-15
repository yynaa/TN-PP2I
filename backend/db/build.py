import sqlite3
from run_query import run_query

connexion = sqlite3.connect('database.db')
cursor = connexion.cursor()

db_path = 'database.db'

run_query(db_path,'''
    CREATE TABLE IF NOT EXISTS Buildings
        ([building_id] INTEGER PRIMARY KEY, [building_name] VARCHAR, [address] VARCHAR, [GPS_lat] REAL, [GPS_long] REAL, [evaluation] INTEGER) I          
    ''')
run_query(db_path,'''
    CREATE TABLE IF NOT EXISTS Users
        ([login] VARCHAR PRIMARY KEY, [email] VARCHAR, [password] VARCHAR, [display_name] VARCHAR, [creation_date] DATE)
    ''')
run_query(db_path,'''
    CREATE TABLE IF NOT EXISTS Reviews
        ([review_id] INTEGER PRIMARY KEY, [user_login] VARCHAR, [content] VARCHAR)
    ''')