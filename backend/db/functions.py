import sqlite3
from math import*
from core import columns_names_buildings, columns_names_users,columns_names_reviews 

# -------------------------------------------------------------------

def run_query(db_path:str,query:str)->None:
    """Runs the given query, using the given database.
    
    Args:
        db_path (str):  Path of the database.
        query (str):    Query you want to run.
    """

    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()

    cursor.execute(query)

    connexion.commit()
    connexion.close()

    return

# -------------------------------------------------------------------

def fetch_Data(db_path:str,table_name:str)->list[dict]:
    """Returns the list of all rows in the given table in the given database
    as dictionnaries, containing as keys the names of the column, and as values
    the attribute values.

    Args:
        db_path (str): Path of the database.
        table_name (str): Table name whose informations you want access to.

    Returns:
        list[dict]: list of all rows in the given table in the given database
    as dictionnaries :
                keys = names of the column, values = the attribute values.
        If there is no table named after the given name in the given database,
            the function returns the empty list.
    """

    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()

    if table_name == "Buildings":
        column_list = columns_names_buildings
    elif table_name == "Users":
        column_list = columns_names_users
    elif table_name == "Reviews":
        column_list = columns_names_reviews
    else:
        return []

    select_query = "SELECT * FROM " + table_name

    cursor.execute(select_query)

    rows = cursor.fetchall()
    returned_list = []
    for row in rows:
        dictionnary = {}
        for i in range(len(row)):
            dictionnary[column_list[i]] = row[i]
        returned_list.append(dictionnary)

    connexion.close()

    return returned_list

# -------------------------------------------------------------------

def nearest_building(db_path:str,building_name:str)->str:
    """Returns the name of the nearest building to the given target.

    Args:
        db_path (str): Path of the database.
        building_name (str): Name of the targetted building.

    Returns:
        str: Name of the nearest building to the given target.
    """

    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()

    cursor.execute("SELECT GPS_lat,GPS_long FROM Buildings WHERE building_name = '" + building_name + "'")
    coord_target = cursor.fetchall()[0]

    square_of_search_size = 1
    nearest = None
    nearest_distance = inf

    while nearest == None:

        square_of_search = str(coord_target[0] - square_of_search_size) + " < GPS_lat AND GPS_lat < " + str(coord_target[0] + square_of_search_size) + " AND " + str(coord_target[1] - square_of_search_size) + " < GPS_long AND GPS_long < " + str(coord_target[1] + square_of_search_size)
        cursor.execute("SELECT building_name,GPS_lat,GPS_long FROM Buildings WHERE " + square_of_search + ";")
        building_within_reach = cursor.fetchall()

        for i in building_within_reach:
            distance = sqrt((coord_target[0]-i[1])**2+(coord_target[1]-i[2])**2)
            if distance < nearest_distance and i[0] != building_name:
                nearest_distance = distance
                nearest = i[0]
        square_of_search_size += 1

    connexion.close()

    return nearest

# -------------------------------------------------------------------

if __name__ == "__main__":

    db_path = "database.db"

    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Mairie','     ',45.4,60.1,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Gym','        ',145.6,60.9,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('College','    ',44.6,159.2,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Tour','       ',40.6,160.9,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Chateau','    ',45.6,64.9,100);")


    # print(fetch_Data(db_path,'Buildings'))
    print(nearest_building(db_path,'Mairie'))

    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Mairie';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Gym';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'College';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Tour';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Chateau';")
    # print(fetch_Data(db_path,'Buildings'))


    pass