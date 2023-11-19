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

def fetch_Data_buildings(db_path:str,building_id:int)->dict:
    """Quite similar to the fetch_Data function. Returns the dictionnary registering
    all the information about the given building.
    Note: this function only works for the 'Buildings' table.

    Args:
        db_path (str): Path of the database.
        building_id (int): ID of the building you want information about.

    Returns:
        dict: dictionnary registering all the information about the given building :
                keys = names of the column, values = the attribute values.
        If there is no building named after the given name in the given database,
            the function returns the empty dictionnary.
    """

    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()

    select_query = "SELECT * FROM Buildings WHERE building_id = " + str(building_id)
    cursor.execute(select_query)
    content = cursor.fetchall()

    if content == []:
        return {}

    element_to_return = content[0]
    dictionnary = {}
    for i in range(len(element_to_return)):
        dictionnary[columns_names_buildings[i]] = element_to_return[i]

    connexion.close()

    return dictionnary

def fetch_Data_user(db_path:str,user_login:str)->dict:
    """Quite similar to the fetch_Data function. Returns the dictionnary registering
    all the information about the given User.
    Note: this function only works for the 'Users' table.

    Args:
        db_path (str): Path of the database.
        user_login (str): Login of the User you want information about.

    Returns:
        dict: dictionnary registering all the information about the given user :
                keys = names of the column, values = the attribute values.
        If there is no user named after the given login in the given database,
            the function returns the empty dictionnary.
    """

    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()

    select_query = "SELECT * FROM Users WHERE login = '" + user_login + "';"
    cursor.execute(select_query)
    content = cursor.fetchall()

    if content == []:
        return {}

    element_to_return = content[0]
    dictionnary = {}
    for i in range(len(element_to_return)):
        dictionnary[columns_names_users[i]] = element_to_return[i]

    connexion.close()

    return dictionnary

# -------------------------------------------------------------------

def building_search_byname(db_path:str,building_name:str,GPS_lat:float,GPS_long:float,number_of_instances=10)->list[int]:
    """Returns the list of the id of the buildings whose name contains the given building_name, sorted by distance from
    the given GPS coordinates. The maximum size of the list can be modified, but its default value is 10.

    Args:
        db_path (str): Path of the database.
        building_name (str): Name of the building(s) you want.
        GPS_lat (float): Latitude of the origin (used to sort the locations by distance).
        GPS_long (float): Longitude of the origin (used to sort the locations by distance).
        number_of_instances (int, optional): Number of instances in the final list. Defaults to 10.

    Returns:
        list[int]: List of the id of the buildings whose name contains the given building_name, sorted
                by distance from the given GPS coordinates.
    """

    def building_search_byname(db_path:str,building_name:str)->list[int]:
        connexion = sqlite3.connect(db_path)
        cursor = connexion.cursor()

        all_buildings = fetch_Data(db_path,'Buildings')
        returned_list = []

        for building in all_buildings:
            if building_name in building['building_name']:
                returned_list.append(building['building_id'])
        
        connexion.close()

        return returned_list

    search_by_name = building_search_byname(db_path,building_name)
    search_by_name_unsorted = []
    for build_id in search_by_name:
        building_fullinfo = fetch_Data_buildings(db_path,build_id)
        lat,long = building_fullinfo['GPS_lat'],building_fullinfo['GPS_long']
        distance_to_origin = sqrt((lat-GPS_lat)**2+(long-GPS_long)**2)
        search_by_name_unsorted.append([build_id,distance_to_origin])

    # Tri
    search_by_name_sorted = search_by_name_unsorted[:]
    left,right = 0,len(search_by_name_sorted)-1
    for i in range(left+1,right+1):
        key_item = search_by_name_sorted[i]
        j = i-1
        while j >= left and search_by_name_sorted[j][1] > key_item[1]:
            search_by_name_sorted[j+1] = search_by_name_sorted[j]
            j -=1
        search_by_name_sorted[j+1] = key_item

    if number_of_instances < len(search_by_name_sorted):
        maximum_length = number_of_instances
    else:
        maximum_length = len(search_by_name_sorted)
    returned_list_with_sizelimit = []
    for i in range(maximum_length):
        returned_list_with_sizelimit.append(search_by_name_sorted[i][0])

    return returned_list_with_sizelimit

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

def create_User(db_path:str,login:str,email:str,password:str,display_name:str,year:int,month:int,day:int)->list:
    """Create a User using the given information. For the account to be created, the database must not already have
        an account with the given login, nor the given email (these are primary keys).

    Args:
        db_path (str): Path of the database.
        login (str): Login of the User (must be unique in the table).
        email (str): Email of the User (must be unique in the table).
        password (str): Password of the User.
        display_name (str): Display name of the User.
        year (int): Year of creation of the account.
        month (int): Month of creation of the account.
        day (int): Day of creation of the account.

    Returns:
        list: [bool , str if needed]: Did the function successfully create the account? If not, why?
    """

    users_db = fetch_Data(db_path,'Users')
    login_found,email_found = False,False
    for i in users_db:
        if i['login'] == login:
            login_found = True
        if i['email'] == email:
            email_found = True
    if login_found:
        return [False, "There is already an account with this login."]
    if email_found:
        return [False, "There is already an account with this email."]

    date = str(year) + "/" + str(month) + "/" + str(day)
    request = "INSERT INTO Users VALUES ('" + login + "','" + email + "','" + password + "','" + display_name + "','" + date + "');"

    run_query(db_path,request)

    return [True]

def check_password(db_path:str,login:str,given_password:str)->list:
    """Updates the password of the given login. The new password must be different
        from the old one.

    Args:
        db_path (str): Path of the Database.
        login (str): Login of the User.
        given_password (str): Password the function will compare to the real password of the given User.

    Returns:
        list: [bool , str if needed]: Is it the right password? If not, is it because there is no such account,
            or because the password is wrong?
    """

    user_data = fetch_Data_user(db_path,login)
    if user_data == {}:
        return [False, "There is no account with this login."]

    if given_password == user_data['password']:
        return [True]
    return [False, "The given password isn't the true password of the account."]

def update_password(db_path:str,login:str,newPassword:str)->list:
    """Updates the password of the given login. The new password must be different
        from the old one.

    Args:
        db_path (str): Path of the Database.
        login (str): Login of the User.
        newPassword (str): New password of the User (must be different from the old one).

    Returns:
        list: [bool , str if needed]: Did the function successfully create the account? If not, why?
    """

    user_data = fetch_Data_user(db_path,login)
    if user_data == {}:
        return [False, "There is no account with this login."]
    if newPassword == user_data['password']:
        return [False, "The old password and the new one are the same."]

    run_query(db_path,"UPDATE Users SET password = '" + newPassword + "' WHERE login = '" + login + "';")

    return [True]

def remove_User(db_path:str,login:str)->list:
    """Removes the given User from the database.

    Args:
        db_path (str): Path of the Database.
        login (str): Login of the User you want to remove.

    Returns:
        list: [bool , str if needed]: Did the function successfully create the account? If not, why?
    """

    user_data = fetch_Data_user(db_path,login)
    if user_data == {}:
        return [False, "There is no account with this login."]
    
    run_query(db_path,"DELETE FROM Users WHERE login = '" + login + "';")

    return [True]

# -------------------------------------------------------------------

if __name__ == "__main__":

    db_path = "database.db"

    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Mairie','Nancy',45.4,60.1,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Gym','        ',145.6,60.9,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('College','    ',44.6,159.2,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Tour','       ',40.6,160.9,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Chateau','    ',45.6,64.9,100);")
    run_query(db_path,"INSERT INTO Buildings (building_name,address,GPS_lat,GPS_long,evaluation) VALUES ('Mairie','Maîche',0,160.1,100);")

    run_query(db_path, "INSERT INTO Users (login,email,password,display_name,creation_date) VALUES ('albert','albertdu95@tamereenshort.com','1234','Albert Dantamèr','2023/11/19');")

    print(fetch_Data(db_path,'Users'))
    print(remove_User(db_path,'alber'))
    print(fetch_Data(db_path,'Users'))

    run_query(db_path,"DELETE FROM Users WHERE login = 'albert';")
    run_query(db_path,"DELETE FROM Users WHERE login = 'alber';")

    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Mairie';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Gym';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'College';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Tour';")
    run_query(db_path,"DELETE FROM Buildings WHERE building_name = 'Chateau';")

    pass

# -------------------------------------------------------------------
"""
Next function to be implemented:
        Fct qui renvoie que les batiments présent dans une certaine zone autour du User
                        Entrées : GPS + côté du carré de recherche

"""