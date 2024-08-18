from config import app, db
from models import Contact, Resource, Building, CurrentlyBuilding
from flask import request, jsonify
from variableHelpers import initial_variables
import citizenActions
import random
import buildings
import country

@app.route("/advance", methods=["PATCH"])
def advance():
    citizenActions.eat()   ##### adjusts health as well #####
    healthFactor = Contact.query.get(13).value * 0.01 
    strength = Contact.query.get(18)
    seasonObj = Contact.query.get(8)
    season = seasonObj.value
    strength.value  = round(40 + 0.6* 100*healthFactor,2)
    db.session.commit()
    citizenActions.build() ### including builders
    country.advance()
    #cooks
    toAdd = 0
    cookingPower = citizenActions.CooksEff()[2]
    wheat = Resource.query.get(2)
    wheat.value -= cookingPower
    left = wheat.value  # wheat left after making the change
    if left < 0:
        toAdd = left
    wheat.value -= toAdd
    bread = Resource.query.get(6)
    bread.value += cookingPower + toAdd

    #Butchers
    toAdd = 0
    butcherPower = citizenActions.ButcherEff()[2]
    rawMeat = Resource.query.get(4)
    rawMeat.value -= butcherPower
    left = rawMeat.value
    if left < 0:
        toAdd = left
    rawMeat.value -= toAdd
    cookedMeat = Resource.query.get(7)
    cookedMeat.value += butcherPower + toAdd
    
    #Hunters
    hunterPower = citizenActions.HunterEff()[8]
    rawMeat.value += hunterPower
    fur = Resource.query.get(3)
    fur.value += hunterPower

    #Loggers
    wood = Resource.query.get(5)
    loggerPower = citizenActions.LoggerEff()[6]
    wood.value += loggerPower

    #Planters(Farmers)
    planted = Contact.query.get(10)
    farmerPower = citizenActions.farmerEff(season)[0]
    if((season)%4 == 1): #Spring
        planted.value += farmerPower
    elif(season == 2):
        berries = Resource.query.get(8)
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

    buildings.advanceBuildings()

    population = Contact.query.get(5)

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
        available = Contact.query.get(6)
        available.value -= fallOff
        print(" AVAILABILE VALUE ", available.value)
        if (available.value < 0):
            leftover = round(available.value * -1,0)
            index = 0
            for i in initial_variables:
                index += 1
                if i['type'] == 'JOB':
                    toSubtract = Contact.query.get(index)
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
                for j in Building.query.all():
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

    week = Contact.query.get(7) # move time forward
    week.value += 1
    week.value = round(week.value, 0)
    if week.value == 14:
        season = Contact.query.get(8)
        week.value = 1
        season.value += 1
        season.value = round(season.value, 0)
        if season.value == 4:
            season.value = 0
            year = Contact.query.get(9)
            year.value += 1
            year.value = round(year.value,0)

    db.session.commit()
    return jsonify({"message": "advanced...."}), 201

@app.route("/advancePackage", methods=['GET'])
def advancePackage():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})