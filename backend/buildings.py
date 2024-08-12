from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork




def housingCapacity():
    logCabin = Building.query.get(1)
    return logCabin.value * logCabin.capacity
