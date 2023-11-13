from fastapi import APIRouter
from db_config import users
from passlib.context import CryptContext
from request_body import User
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from schemas import getalluserrs,getoneuser

signups = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@signups.post("/signup")
def signin(inputuser:User):
    inputuser.password = pwd_context.hash(inputuser.password)
    try:
        input_user = inputuser.dict()
        # print(input_user)
        result = users.insert_one(input_user)
        id = str(result.inserted_id)
        print(result.inserted_id)
        return {"status":"Added Succesfuly","id":id}
    except:
        return "Failed to add"
    

@signups.get("/getalluser")
def getusers():
    all_data = (list(users.find()))
    return getalluserrs(all_data)

@signups.get("/getuser/{id}")
def getuser(id:str):
    all_data = users.find_one({"_id":ObjectId(id)})
    # print(all_data)
    return getoneuser(all_data)

    

