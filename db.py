from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
# make a new table in client
db=client["habit_tracker"]

habit_cols=db["habits"]
log_cols=db["logs"]

print(db.list_collection_names())