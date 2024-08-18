from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
from config import app, db
from flask import request, jsonify


namesToIDs = {}

def housingCapacity():
    logCabin = Building.query.get(1)
    return logCabin.value * logCabin.capacity

def reactToBuildings(buildingsBuiltThisWeek):
    for key in buildingsBuiltThisWeek:
        CurrentlyBuilding = Building.query.get(key)
        if CurrentlyBuilding.working is not None:
            cpw = CurrentlyBuilding.working
            maximum = CurrentlyBuilding.value * CurrentlyBuilding.capacity
            CurrentlyBuilding.working =  {'value': int(cpw['value']), 'maximum': int(maximum), 'minimum': int(cpw['minimum'])}
            db.session.add(CurrentlyBuilding)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def buildingsEff(building, outputPower=0):
    strength = round(Contact.query.get(18).value * 0.01,2)
    NoToolEfficiency = building.tools['None']
    count = building.working['value']
    toolOfNote = building.tools['With']
    tool = (Resource.query.get(toolOfNote[0]))
    toolName = tool.name
    toolMax = int(tool.value)
    toolEfficiency = toolOfNote[1]
    baseEfficiency = building.tools['Base']
    otherFactors = []
    if toolMax >= count:
        UsingTool = count
    else:
        UsingTool = toolMax
    UsingNoTools = int(count - UsingTool)
    if count != 0:
        totalEfficiency = baseEfficiency  * strength * ( ((toolEfficiency * UsingTool)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency  * toolEfficiency * strength
    if outputPower != 0:
        return totalEfficiency * count
    return toolEfficiency, UsingTool, UsingNoTools, NoToolEfficiency, totalEfficiency, count, baseEfficiency, otherFactors, toolName, strength

def advanceBuildings():
    buildings = Building.query.all()
    for buildingCurr in buildings:
        if buildingCurr.working is not None:  ####### Action involving workers
            print("THIS ACTUALLY HAS AN ACTION I SUPPOSE", buildingCurr.working)
            if  buildingCurr.Inputs:
                print("SEE HOW MUCH WE CAN DO")
                input = buildingCurr.Inputs


                output = buildingCurr.Outputs
                buildingPower = buildingsEff(buildingCurr, 1)
                
                for key in input:
                    print("key : ", key)
                    resource = Resource.query.get(int(key))
                    print("BUIDLING POWER ", buildingPower, "    resourcevalue ",resource.value, "   ",  input[key])
                    print(resource.value * input[key])
                    if resource.value  < buildingPower *  input[key]:
                        print((resource.value ) , "  evse  ", buildingPower *  input[key] )
                        ratio = resource.value / (buildingPower*input[key])
                        print("ratio ", ratio)
                    buildingPower  *=  ratio
                for key in input:
                    print("BEF", buildingPower)
                    resource = Resource.query.get(int(key))
                    resource.value -= buildingPower * input[key]

                for key in output:
                    print("BEF", buildingPower)
                    print("key : ", key)
                    resource = Resource.query.get(int(key))
                    resource.value += buildingPower * output[key]
                    print("value ", output[key])





            else:


                    # wood = Resource.query.get(5)
                    # loggerPower = citizenActions.LoggerEff()[6]
                    # wood.value += loggerPower

                print("DONT WORRY")
                print(buildingCurr)
                print(buildingCurr.Outputs)
                if buildingCurr.Outputs:
                    print("OUT")
                    output = buildingCurr.Outputs
                    buildingPower = buildingsEff(buildingCurr, 1)
                    for key in output:
                        print("BEF", buildingPower)
                        print("key : ", key)
                        resource = Resource.query.get(int(key))
                        resource.value += buildingPower * output[key]
                        print("value ", output[key])