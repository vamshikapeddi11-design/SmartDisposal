from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/bin")
def get_bin_data():

    data = bins.find_one({}, {"_id": 0})

    if data:
        return data

    return {
        "current_level": 0,
        "history": []
    }
