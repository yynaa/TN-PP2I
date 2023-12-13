import sqlite3
from enum import IntEnum, auto

# -------------------------------------------------------------------

class Tags(IntEnum):
    entrance_fauteuilRoulant = auto()
    toilets_fauteuilRoulant = auto()
    seat_fauteuilRoulant = auto()
    # ...

# -------------------------------------------------------------------

connexion = sqlite3.connect('backend/db/database.db')
cursor = connexion.cursor()

db_path = 'backend/db/database.db'

# CREATING ALL THE TABLE IN THE DB

cursor.execute("DROP TABLE Buildings")
cursor.execute("DROP TABLE Users")
cursor.execute("DROP TABLE Reviews")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buildings
        ([building_id] INTEGER PRIMARY KEY NOT NULL, [building_name] VARCHAR, [class] VARCHAR, [address] VARCHAR, [GPS_lat] REAL, [GPS_long] REAL, [evaluation] INTEGER, [tags] INTEGER)          
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
        ([login] VARCHAR, [email] VARCHAR, [password] VARCHAR, [display_name] VARCHAR, [creation_date] DATE, PRIMARY KEY ([login],[email]))
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reviews
        ([review_id] INTEGER PRIMARY KEY NOT NULL, [user_login] VARCHAR NOT NULL, [content] VARCHAR, [building_id] INTEGER NOT NULL, [upload_date] DATE)
    ''')

columns_names_buildings = ["building_id","building_name","class","address","GPS_lat","GPS_long","evaluation", "tags"]
columns_names_users = ["login","email","password","display_name","creation_date"]
columns_names_reviews = ["review_id","user_login","content","building_id","upload_date"]

if __name__ == "__main__":
    with open("db_content.txt","r") as file:
        content = file.read().split("§\n")
        title_list = content[0]
        tag_list = content[1]
        content.remove(title_list)
        content.remove(tag_list)
        for i in content:
            i = i.split(",")
            tags = i[-1]
            tag_value  = 0
            for j in tags:
                if j == "<Entrée accessible aux personnes en fauteuil roulant>":
                    tag_value += Tags.entrance_fauteuilRoulant.value
                elif j == "<Toilettes accessibles aux personnes en fauteuil roulant>":
                    tag_value += Tags.toilets_fauteuilRoulant.value
                elif j == "<Sièges accessibles aux personnes en fauteuil roulant>":
                    tag_value += Tags.seat_fauteuilRoulant.value
            
            i_list = []
            if len(i) >= 3:
                for j in i:
                    j = list(j)
                    j.pop(0)
                    j.pop()
                    j_final = ""
                    for k in j:
                        j_final += k
                    i_list.append(j_final)
                cursor.execute('''
                    INSERT INTO Buildings (building_name,class,address,GPS_lat,GPS_long,evaluation,tags) VALUES (?,?,?,?,?,100,?);
                               ''', (i_list[0],i_list[1],i_list[2],i_list[3],i_list[4],tag_value))
                connexion.commit()

connexion.close()