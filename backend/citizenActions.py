
from config import app, db
from models import Contact, Resource
from flask import request, jsonify
from variableHelpers import initial_variables
nFoodTypes = 0

@app.route("/eat", methods=["PATCH"])
def eat():
    global foodTypes
     # take rationing percentage from some db.. it will be saved in some DB
    rationingPval = Contact.query.get(12).value
    expectedFood = rationingPval * 0.01 * Contact.query.get(5).value * 0.02
    eatHelper(expectedFood)
    HealthEquilibrium = rationingPval*0.01 * (68+nFoodTypes*8)
    HealthCurrent = Contact.query.get(13)

    
    HealthCurrent.value = round(HealthEquilibrium,0)

    db.session.commit()

    return jsonify({"message": " Values updated"}), 201

def eatHelper(expectedFood):
    global nFoodTypes
    FoodTypeValues = [0,0,0,0]
    nFoodTypes = 0
    # fruits, vegtables, meat, grain        
    FoodTypeValues[0] = Resource.query.get(8).value
    FoodTypeValues[1] = Resource.query.get(9).value
    FoodTypeValues[2] = Resource.query.get(7).value
    FoodTypeValues[3] = Resource.query.get(6).value
   # print("Expected  ", FoodTypeValues)
                                                                         # Only do one food for each value needs to be updated in the futrere/////////////////////
    foodmin = 9999999
    for FoodVal in FoodTypeValues:
        if FoodVal > 0:
            nFoodTypes += 1
            if FoodVal < foodmin:
                foodmin = FoodVal
    if nFoodTypes == 0:
        return 
 #   print(nFoodTypes, "  ", foodmin, " ", expectedFood, " ", expectedFood/nFoodTypes)
    # now subtract the lesser of food min and 
    if foodmin >= expectedFood/nFoodTypes:
        change = expectedFood/nFoodTypes
        val8  = Resource.query.get(8)
        val7 = Resource.query.get(7)
        val6 = Resource.query.get(6)
        val9 = Resource.query.get(9)
        val8.value -= change
        val9.value -= change
        val7.value -= change
        val6.value -= change
        if val8.value < 0:
            val8.value = 0
        if val9.value < 0:
            val9.value = 0
        if val7.value < 0:
            val7.value = 0
        if val6.value < 0:
            val6.value = 0
         
    else :
        #
        change = foodmin
        foodleft = expectedFood - foodmin*4
        val8  = Resource.query.get(8)
        val7 = Resource.query.get(7)
        val6 = Resource.query.get(6)
        val9 = Resource.query.get(9)
        val8.value -= change
        val9.value -= change
        val7.value -= change
        val6.value -= change
        if val8.value < 0:
            val8.value = 0
            foodleft += foodmin
        if val9.value < 0:
            val9.value = 0
            foodleft += foodmin
        if val7.value < 0:
            val7.value = 0
            foodleft += foodmin
        if val6.value < 0:
            val6.value = 0
            foodleft += foodmin
        print(foodleft)
        eatHelper(foodleft)

    db.session.commit()

