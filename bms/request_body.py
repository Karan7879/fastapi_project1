from pydantic import BaseModel
from typing import List,Union,Dict
from enum import Enum as PydanticEnum
from datetime import datetime

class UserRole(str, PydanticEnum):
    customer = "customer"
    owner = "owner"
    admin = "admin"

class UserCreate(BaseModel):
    username :str
    password :str
    email :str
    position : UserRole
    full_name : str

class AddMultiplex(BaseModel):
    multiplex_name :str
    audi_count :int
    owner :str
    owner_email :str

class AuditoriumCreate(BaseModel):
    auditorium_name: str
    seats_count: int
    seats_arrangement: Dict[str,List[int]]
    multiplex_id: int
    # [A]

class ShowCreate(BaseModel):
    show_name :str
    auditorium_id :Union[int,None]
    multiplex_id : Union[int,None]
    startdate : datetime
    enddate : datetime
    pricing: Dict[str,float]

class Bookings(BaseModel):
    seat_number : str
    # seat_number_j : int
    # Need to add how if user has booked ticket for multiple user
    booking_time : datetime
    cancel_time : datetime
    show_name : str
    show_id : int
    
    # audi_name : str
    # multiplex_name : str
    # user_id : str


    
