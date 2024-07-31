from config import app, db
from models import Contact, Resource, Building, CurrentlyBuilding
from flask import request, jsonify
from variableHelpers import initial_variables
import citizenActions
import random
@app.route("/advance", methods=["PATCH"])
def advance():
    citizenActions.eat()   
    healthFactor = Contact.query.get(13).value * 0.01 
    citizenActions.build()


    #cooks
    toAdd = 0
    cooks = Contact.query.get(3)
    cookingPower = cooks.value * 0.1 * healthFactor
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
    butchers = Contact.query.get(11)
    butcherPower = butchers.value * 0.1 * healthFactor
    rawMeat = Resource.query.get(4)
    rawMeat.value -= butcherPower
    left = rawMeat.value
    if left < 0:
        toAdd = left
    rawMeat.value -= toAdd
    cookedMeat = Resource.query.get(7)
    cookedMeat.value += butcherPower + toAdd
    

    #Hunters
    hunters = Contact.query.get(2)
    change = hunters.value * 0.1  * healthFactor
    rawMeat.value += change
    fur = Resource.query.get(3)
    fur.value += change

    #Loggers
    loggers = Contact.query.get(4)
    wood = Resource.query.get(5)
    wood.value += loggers.value * 0.1  * healthFactor

    #Planters(Farmers)
    planters = Contact.query.get(1)
    seasonObj = Contact.query.get(8)
    season = seasonObj.value
    planted = Contact.query.get(10)
    farmerPower = planters.value * 0.1  * healthFactor
    if((season)%4 == 1): #Spring
        planted.value += farmerPower
    elif((season)%4 == 3):
        toAdd = 0
        planted.value -= farmerPower
        if planted.value < 0:
            toAdd = planted.value
            planted.value -= toAdd
        wheat.value += farmerPower + toAdd
    elif((season)%4 == 0):
        planted.value = 0


    population = Contact.query.get(5)

    if healthFactor < 0.50:
        percentOff = 0
        diff = (0.6 - healthFactor) *0.5    
        if healthFactor < 0.25:
            diff += (0.25 - healthFactor)*3 # 
            if healthFactor < 0.1:
                diff += (0.1 - healthFactor)*6
        percentOff = diff  * random.randint(10,30) * 0.01 # 5-15,
        oldPop = population.value
        population.value = round(population.value * (1-percentOff),0)
        fallOff =  oldPop - population.value
        available = Contact.query.get(6)
        available.value -= fallOff

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