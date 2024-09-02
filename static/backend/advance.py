import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, user, contactOffset,resourceOffset,buildingOffset,countryOffset
from flask import request, jsonify
from static.backend.variableHelpers import initial_variables
import static.backend.citizenActions as citizenActions
import static.backend.buildings as buildings
import static.backend.country as country
import random

@app.route("/advance/<string:currUserName>", methods=["PATCH"])
def advance(currUserName):
    offset = user.query.get(currUserName).id
    citizenActions.eat(currUserName)   ##### adjusts health as well #####
    healthFactor = Contact.query.get(13 + offset*contactOffset).value * 0.01 
    strength = Contact.query.get(18 + offset*contactOffset)
    seasonObj = Contact.query.get(8 + offset*contactOffset)
    season = seasonObj.value
    strength.value  = round(40 + 0.6* 100*healthFactor,2)
    db.session.commit()
    citizenActions.build(currUserName) ### including builders
    country.advance(currUserName)
    #cooks
    toAdd = 0
    cookingPower = citizenActions.CooksEff(currUserName)[2]
    wheat = Resource.query.get(2 + offset*resourceOffset)
    wheat.value -= cookingPower
    left = wheat.value  # wheat left after making the change
    if left < 0:
        toAdd = left
    wheat.value -= toAdd
    bread = Resource.query.get(6 + offset*resourceOffset)
    bread.value += cookingPower + toAdd

    #Butchers
    toAdd = 0
    butcherPower = citizenActions.ButcherEff(currUserName)[2]
    rawMeat = Resource.query.get(4 + offset*resourceOffset)
    rawMeat.value -= butcherPower
    left = rawMeat.value
    if left < 0:
        toAdd = left
    rawMeat.value -= toAdd
    cookedMeat = Resource.query.get(7 + offset*resourceOffset)
    cookedMeat.value += butcherPower + toAdd
    
    #Hunters
    hunterPower = citizenActions.HunterEff(currUserName)[8]
    rawMeat.value += hunterPower
    fur = Resource.query.get(3 + offset*resourceOffset)
    fur.value += hunterPower

    #Loggers
    wood = Resource.query.get(5 + offset*resourceOffset)
    loggerPower = citizenActions.LoggerEff(currUserName)[6]
    wood.value += loggerPower

    #Planters(Farmers)
    planted = Contact.query.get(10 + offset*contactOffset)
    farmerPower = citizenActions.farmerEff(season,currUserName)[0]
    if((season)%4 == 1): #Spring
        planted.value += farmerPower
    elif(season == 2):
        berries = Resource.query.get(8 + offset*resourceOffset)
        berries.value += farmerPower
    elif((season)%4 == 3):
        toAdd = 0
        planted.value -= farmerPower
        if planted.value < 0:
            toAdd = planted.value
            planted.value -= toAdd
        wheat.value += farmerPower + toAdd
    elif((season)%4 == 0):
        planted.value = 0

    buildings.advanceBuildings(currUserName)

    population = Contact.query.get(5 + offset*contactOffset)

    if healthFactor < 0.50:
        percentOff = 0
        diff = (0.6 - healthFactor) *0.6    
        if healthFactor < 0.25:
            diff += (0.3 - healthFactor)*4 # 
            if healthFactor < 0.1:
                diff += (0.1 - healthFactor)*5
        percentOff = diff  * random.randint(10,30) * 0.01 # 5-15,
        oldPop = population.value
        population.value = round(population.value * (1-percentOff),0)
        fallOff =  oldPop - population.value
        available = Contact.query.get(6 + offset*contactOffset)
        available.value -= fallOff
        print(" AVAILABILE VALUE ", available.value)
        if (available.value < 0):
            leftover = round(available.value * -1,0)
            index = 0
            for i in initial_variables:
                index += 1
                
                if i.get('type') == 'JOB':
                    toSubtract = Contact.query.get(index + offset*contactOffset)
                    toSubtract.value -= leftover
                    leftover = 0 
                    if (toSubtract.value < 0):
                        leftover -= toSubtract.value
                        toSubtract.value -= toSubtract.value
                        leftover = round(leftover,0)
                    db.session.add(toSubtract)
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
            if leftover > 0:
                for j in Building.query.filter(Building.currUserName == currUserName).all():
                    print("j ", j)
                    if j.working != None:
                        print(j.working)
                        print("JWOKRVALUE " ,  j.working['value'])
                        j.working['value'] -= leftover
                        leftover = 0
                        if (j.working['value'] < 0):
                            leftover -= j.working['value'] 
                            j.working['value']  -= j.working['value'] 
                            leftover = round(leftover,0)
                        print("  JJJJ ", j.working)
                        newWork = {'value': j.working['value'], 'maximum': j.working['maximum'], 'minimum': j.working['minimum']}
                        print ("newWark", newWork)
                        j.working = {'value': int(j.working['value']), 'maximum': int(j.working['maximum']), 'minimum': int(j.working['minimum'])}
                        db.session.add(j)
                        try:
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            return jsonify({"message": f"An error occurred: {str(e)}"}), 500




            available.value = 0

    week = Contact.query.get(7 + offset*contactOffset) # move time forward
    week.value += 1
    week.value = round(week.value, 0)
    if week.value == 14:
        season = Contact.query.get(8 + offset*contactOffset)
        week.value = 1
        season.value += 1
        season.value = round(season.value, 0)
        if season.value == 4:
            season.value = 0
            year = Contact.query.get(9 + offset*contactOffset)
            year.value += 1
            year.value = round(year.value,0)

    db.session.commit()
    return jsonify({"message": "advanced...."}), 201

@app.route("/advancePackage/<string:currUserName>", methods=['GET'])
def advancePackage(currUserName):
    contacts = Contact.query.filter(Contact.currUserName == currUserName).all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})