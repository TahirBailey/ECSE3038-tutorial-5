
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# Connect to MongoDB using the connection string
client = MongoClient(os.getenv("MONGODB_URI"))

# Select the database and collection
db = client["ecse3038"]
devices = db["tutorial5"]

app = FastAPI()


# Device data model
class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


# Your handlers go below this line.

@app.get("/devices")
def get_devices():
    all_devices = list(devices.find({}, {"_id": 0}))
    return all_devices
