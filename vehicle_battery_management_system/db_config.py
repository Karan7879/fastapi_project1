from pymongo import MongoClient
import json
from bson import ObjectId

client = MongoClient("mongodb+srv://<username>:<pswd>@cluster0.jwi0z9m.mongodb.net/?retryWrites=true&w=majority")

db= client["vms"]
users = db["users"]
stations = db["stations"]
battery = db["batteries"]


# async def get_database():
#     return client


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)