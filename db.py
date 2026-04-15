from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import date
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
# make a new table in client
db=client["habit_tracker"]

habit_cols=db["habits"]
log_cols=db["logs"]

def save_habit(name,days):
    habit={
        "name":name,
        "days":days,
        "start_date":str(date.today()),
        "logs":{}, #{"date":True,"date2":Falsee}
        "current_streak":0,
        "longest_streak":0,
        'total_done':0,
        "completion_rate":0,
    }
    result=habit_cols.insert_one(habit)
    return result.inserted_id
