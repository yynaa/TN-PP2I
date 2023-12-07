import sqlite3

connexion = sqlite3.connect('database.db')
cursor = connexion.cursor()

db_path = 'database.db'

# CREATING ALL THE TABLE IN THE DB
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buildings
        ([building_id] INTEGER PRIMARY KEY NOT NULL, [building_name] VARCHAR, [address] VARCHAR, [GPS_lat] REAL, [GPS_long] REAL, [evaluation] INTEGER, [tags] INTEGER)          
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
        ([login] VARCHAR, [email] VARCHAR, [password] VARCHAR, [display_name] VARCHAR, [creation_date] DATE, PRIMARY KEY ([login],[email]))
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reviews
        ([review_id] INTEGER PRIMARY KEY NOT NULL, [user_login] VARCHAR NOT NULL, [content] VARCHAR, [building_id] INTEGER NOT NULL, [upload_date] DATE)
    ''')

columns_names_buildings = ["building_id","building_name","address","GPS_lat","GPS_long","evaluation"]
columns_names_users = ["login","email","password","display_name","creation_date"]
columns_names_reviews = ["review_id","user_login","content","building_id","upload_date"]

connexion.close()