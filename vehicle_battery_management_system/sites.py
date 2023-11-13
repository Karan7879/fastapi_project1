from fastapi import APIRouter
from db_config import users,stations
from request_body import User,ChargingStation
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder
from schemas import getallsite, getonesite
charginroutes = APIRouter()


@charginroutes.post("/addStations")
def addSites(station:ChargingStation):
    station_data = station.dict()

    # Insert the charging station details into MongoDB
    result = stations.insert_one(station_data).inserted_id

    return{**station.dict(), "_id": str(result)}


@charginroutes.get("/getSites")
def getSites():
    all_data = list(stations.find())
    return getallsite(all_data)
    # return {"all_stations":[ChargingStation(**document) for document in all_data]}

@charginroutes.get("/getsite/{id}")
def getSite(id):
    
    all_data = stations.find_one({"_id":ObjectId(id)})
    # print(all_data)
    return getonesite(all_data)

