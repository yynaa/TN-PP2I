import sqlite3

connexion = sqlite3.connect("database")
cursor = connexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buildings
        ([building_id] INTEGER PRIMARY KEY, [building_name] VARCHAR, [address] VARCHAR, [GPS_lat] REAL, [GPS_long] REAL, [evaluation] INTEGER)           
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
        ([login] VARCHAR PRIMARY KEY, [email] VARCHAR, [password] VARCHAR, , [display_name] VARCHAR, [creation_date] DATE)
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reviews
        ([review_id] INTEGER PRIMARY KEY, [user_login] VARCHAR, )
    ''')

connexion.commit()