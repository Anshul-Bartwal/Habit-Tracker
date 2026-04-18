from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import date,timedelta
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"),tlsAllowInvalidCertificates=True)
# make a new table in client
db=client["habit_tracker"]
print("yotest")
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

def update_check(habit_id,date_str,checked,days):
    habit=habit_cols.find_one({"_id":habit_id})

    #update logs
    logs=habit.get("logs",{})
    logs[date_str]=checked

    #recalculate total
    total_done=sum(1 for v in logs.values() if v)

    #recalc current streak
    current_streak=0
    today=date.today()
    for i in range (days):
        d=today-timedelta(days=i)
        key=d.isoformat()
        if logs.get(key):
            current_streak+=1
        else:
            break
    # we iterate from i=0 to number of days so our d=today-timedelta(days=i) goes from today ,today-1,today-2 till today-today then it breaks 
    # recalculate longest streak
    longest_streak=habit.get("longest_streak",0)
    if (current_streak>longest_streak):
        longest_streak=current_streak

    days_elapsed=(today-date.fromisoformat(habit["start_date"])).days+1
    completion_rate=round((total_done/days_elapsed)*100,2)

    habit_cols.update_one({"_id":habit_id},
                          {"$set":{
                              "logs":logs,
                              "current_streak": current_streak,
                              "longest_streak": longest_streak,
                              "total_done": total_done,
                              "completion_rate": completion_rate
                          }})
    
def load_habits():
    ids = [doc["_id"] for doc in habit_cols.find({}, {"_id": 1})]
    result = []
    for id in ids:
        doc = habit_cols.find_one({"_id": id})
        if doc:
            result.append(doc)
    return result
def delete_habit(habit_id):
    habit_cols.delete_one({"_id":habit_id})

# from bson import ObjectId
result =load_habits()
# ann array ofobject 
print(load_habits(),sep='\n')
delete_habit(result[0].get("_id"))


