# from backend.db.core import*
from backend.db.functions import*


db_path = "backend/db/database.db"
print(fetch_Data(db_path,"Users"))