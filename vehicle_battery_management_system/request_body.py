from pydantic import BaseModel,Field,validator
from typing import List,Dict,Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId
from pymodm import fields, MongoModel, connect

class PyObjectId(ObjectId):
    """Custom class to use ObjectId in Pydantic models."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Battery(BaseModel):
    battery_type: str
    battery_percent:float
    battery_capacity:float
    battery_code:int
    battery_charingtime: datetime
    battery_lastcharge:datetime
    battery_inTime:datetime
    battery_OutTime:datetime
    battery_chargincount:int
    occupied_status:bool
    owner:PyObjectId



class Vehicles(BaseModel):
    vehicle_num:str
    vehicle_name:str
    vehicle_type:str

class UserType(str, Enum):
    STATIONOWNER = "STATION_OWNER"
    VEHICLEOWNER = "VEHICLE_OWNER"


class User(BaseModel):
    username:str 
    password:str
    email:str
    amount:float
    penaulty:Optional[float]
    usertype:UserType
    vehicle:Optional[List[Vehicles]]
    


class RenewableEnergy(str, Enum):
    SOLAR = "Solar"
    HYDRO = "Hydro"
    TIDAL = "Tidal"
    WIND = "Wind"

class NonRenewableEnergy(str, Enum):
    COAL = "Coal"
    NUCLEAR = "Nuclear"
    GAS = "Gas"

class EnergySource(BaseModel):
    renewable_energy: RenewableEnergy
    renewable_energy_charge: float
    non_renewable_energy: NonRenewableEnergy
    non_renewable_energy_charge: float


class ChargingStation(BaseModel):
    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         ObjectId: lambda v: str(v)  # Convert ObjectId to string in Pydantic model
    #     }
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    station_name: str
    active_battery_count:int
    sources: EnergySource
    # batteries: Optional[List[Battery]]






