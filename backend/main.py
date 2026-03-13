from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")

db = client.smart_disposal

users = db.users
bins = db.bin_levels


@app.post("/login")
def login(user: dict):

    db_user = users.find_one({
        "email": user["email"],
        "password": user["password"]
    })

    if db_user:
        return {"message":"Login successful"}

    return {"message":"Invalid login"}



@app.get("/bin-data")
def bin_data():

    latest = bins.find_one(sort=[("_id",-1)])

    history = []

    for item in bins.find().sort("_id",-1).limit(5):

        history.append({
            "time":item["time"],
            "level":item["level"]
        })

    return {
        "current_level":latest["level"],
        "history":history
    }
