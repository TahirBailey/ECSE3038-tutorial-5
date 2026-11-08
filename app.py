
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

@app.get("/devices/{name}")
def get_device(name: str):
    device = devices.find_one({"name": name}, {"_id": 0})

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return device

@app.post("/devices", status_code=201)
def create_device(device: Device):

    # Check if a device with this name already exists
    existing_device = devices.find_one({"name": device.name})

    if existing_device is not None:
        raise HTTPException(status_code=409, detail="Device already exists")

    # Convert the device information into a dictionary
    new_device = device.model_dump()

    # Insert the device into MongoDB
    devices.insert_one(new_device)

    # Return the newly created device
    return new_device