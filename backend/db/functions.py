import sqlite3
import pandas as pd
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

if __name__ == "__main__":

    pass