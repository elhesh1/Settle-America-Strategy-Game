from config import app, db
from models import Contact, Resource
from flask import request, jsonify
from variableHelpers import initial_variables

@app.route("/advance", methods=["PATCH"])
def advance():
    #cooks
    print(" ADVANCING ")
    toAdd = 0
    cooks = Contact.query.get(3)
    cookingPower = cooks.value * 0.1
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
    butcherPower = butchers.value * 0.1
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
    change = hunters.value * 0.1
    rawMeat.value += change
    fur = Resource.query.get(3)
    fur.value += change

    db.session.commit()
    return jsonify({"message": "advanced...."}), 201