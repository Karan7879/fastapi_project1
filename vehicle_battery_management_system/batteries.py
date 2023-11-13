
from fastapi import APIRouter
from db_config import users,stations,battery,CustomJSONEncoder
from request_body import User,ChargingStation
from bson import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from schemas import get_all_batery_data

batt = APIRouter()


@batt.post("/addBattery")
def addBatteris(id,count:int):
    inputarr = []
    _id = ObjectId(id)
    try:
        for i in range(count):

            inputarr.append({"battery_type": "Li-Po",
            "battery_percent":0,
            "battery_capacity":500,
            "battery_code":i,
            "battery_charingtime": datetime.now(),
            "battery_lastcharge":datetime.now(),
            "battery_inTime":datetime.now(),
            "battery_OutTime":datetime.now(),
            "battery_chargincount":1,
            "occupied_status":False,
            "owner":str(_id)})
        input_battry = battery.insert_many(jsonable_encoder(inputarr))
        print(input_battry.inserted_ids)
        return "Succesfully added"
    except:
        return {"status":"Something went wrong"}
    # findallbatt = battery.find({"owner": id})
    # print(input_battry.inserted_ids)
    # return JSONResponse(content=json.dumps(list(findallbatt), cls=CustomJSONEncoder))


@batt.get("/getuserbattery/{id}")
def getSite(id):
    all_data = battery.find({"owner":id})
    print(all_data)
    # for data in all_data:
    #     print(data)
    return get_all_batery_data(all_data)

@batt.get("/getuserbattery")
def getSite():
    all_data = battery.find()
    print(all_data)
    # for data in all_data:
    #     print(data)
    return get_all_batery_data(all_data)