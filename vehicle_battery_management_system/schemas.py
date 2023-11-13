from request_body import EnergySource,User,Battery
def getonesite(item)->dict:
    return{
        "id": str(item.get("_id", "")),
        "station_name": item.get("station_name",""),
        "active_battery_count":item.get("active_battery_count",""),
        "sources": item.get("sources","")
    }


def getallsite(items)->list:
    return[getonesite(item) for item in items]


def getoneuser(item) ->dict:
    # print(item)
    return{
    "id": str(item.get("_id", "")),
    "username": item.get("username", ""),
    "email": item.get("email", ""),
    "penalty": item.get("penalty", ""),  # Corrected spelling from 'penaulty'
    "usertype": item.get("usertype", ""),
    "amount": item.get("amount", ""),
    "vehicle": item.get("vehicle", "")
    }
def getalluserrs(items)->list:
    return[getoneuser(item) for item in items]


from datetime import datetime

def map_battery_data(item) -> dict:
    return {
        "battery_type": item.get("battery_type", ""),
        "battery_percent": item.get("battery_percent", 0),
        "battery_capacity": item.get("battery_capacity", 0),
        "battery_code": item.get("battery_code", ""),
        "battery_chargingtime": item.get("battery_chargingtime", datetime.now()),
        "battery_lastcharge": item.get("battery_lastcharge", datetime.now()),
        "battery_inTime": item.get("battery_inTime", datetime.now()),
        "battery_OutTime": item.get("battery_OutTime", datetime.now()),
        "battery_chargingcount": item.get("battery_chargingcount", 1),
        "occupied_status": item.get("occupied_status", False),
        "owner": str(item.get("owner", ""))
    }


def get_all_batery_data(items):
    return[map_battery_data(item) for item in items]

