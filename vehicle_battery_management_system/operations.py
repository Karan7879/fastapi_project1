# def newops(userID,stationID):
#     min((charfingrime-currentrim)*,100)


# 1)batteryswaping -> first time, later times
# -> owner change
# -> status consumtion (True)
# -> time change 
# -> 
# 2)batterycharfing -> anyone can do cheaper but time consuimg
# 3)time -> localtime around 7:00 PM Grid ON
# 4) penalty
# 5) in a minute if more than 5 people price hike by 1% and timing
# 6) 

from fastapi  import APIRouter
from db_config import battery
from schemas import map_battery_data
operations = APIRouter()

@operations.post("/AddNewUserBattery")
def add_new_battery(ownerid,userid):
    update_operation = {"owner": userid}  # Replace with the actual field and value

    all_data = battery.find_one_and_update(
        {"owner":ownerid},
        {"$set":update_operation}
        )
    if all_data:
        print(all_data)
        return "Done"
    else:
        return "Owner don't have any available battery"
    

@operations.patch("/swapBattery")
def swap_battery(ownerid,userid):
    users = {"owner":userid}
    owners = {"owner":ownerid}
    userdata = battery.find_one_and_update(
        {"owner":userid},
        {"$set":owners}
    )
    if userdata:
        ownerdata = battery.find_one_and_update(
            {"owner":ownerid},
            {"$set":users}
        )      
        return "Done"
    else:
        return "User not found"









