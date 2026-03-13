from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")

db = client.smart_disposal

users = db.users
bins = db.bin_levels


class Login(BaseModel):
    email: str
    password: str


@app.post("/login")
def login(user: Login):

    db_user = users.find_one({
        "email": user.email,
        "password": user.password
    })

    if db_user:
        return {"message": "Login successful"}

    return {"message": "Invalid email or password"}
