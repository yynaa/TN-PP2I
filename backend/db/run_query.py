import sqlite3

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

    return