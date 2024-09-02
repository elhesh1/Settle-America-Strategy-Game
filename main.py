
# Request returns a Response. status:200 means success
from flask import request, jsonify, Flask, render_template

from config import app, db
from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, Country, user, contactOffset,resourceOffset,buildingOffset,countryOffset
import static.backend.citizenActions
from sqlalchemy import create_engine, Column, Integer, String, func
import static.backend.advance as advance
import static.backend.hover as hover
import static.backend.buildings as buildings
from static.backend.variableHelpers import initial_variables, initial_resources, initial_buildings, initial_countries
from sqlalchemy.exc import IntegrityError
from static.backend.variableHelpersDev import initial_variablesD, initial_buildingsD, initial_resourcesD, initial_countriesD
import static.backend.country as country

def seed_database(currUserName, newV = 0):
    print(" SEEEDING THE DB::::::::   ", currUserName)
    devModeV = 0
    if devModeV == 0:
        iv = initial_variables
        ir = initial_resources
        ib = initial_buildings
        it = initial_countries
    elif devModeV == 1:
        iv = initial_variablesD
        ir = initial_resourcesD
        ib = initial_buildingsD
        it = initial_countriesD
    print("curr user name ", currUserName)
    for v in iv:
        v["currUserName"] = currUserName
    for r  in ir:
        r["currUserName"] = currUserName
    for b in ib:
        b["currUserName"] = currUserName
    for t in it:
        t["currUserName"] = currUserName
    print("Seeding DB:")

    existing_contacts = db.session.query(Contact).filter_by(currUserName=currUserName).all()
    if not existing_contacts:
        print(" ADDING A USER>>>>>>><<<<<<<<ADDING A USER")
        add_user(currUserName, "test", "test")


        for contact_data in iv:
            contact = Contact(**contact_data)
            print("CURRENT CONTACT = ", contact.name)
            try:
                db.session.add(contact)
                db.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                db.session.rollback()
        #  print("COUNTACTS:" , Contact['1'])
        for c in it:
            d = Country(**c)
            try:
                db.session.add(d)
                db.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                db.session.rollback()   


        for a in ir:
            b = Resource(**a)
            try:
                db.session.add(b)
                db.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                db.session.rollback()  

        for buildings in ib:
            building = Building(**buildings)
            try:
                db.session.add(building)
                db.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                db.session.rollback()  
    else:
        print("other")
        print("new ;  ", newV)
        if newV == 1:
            db.session.query(user).filter_by(name=currUserName).delete()
            add_user(currUserName, "test", "test")
            print(" WHY TEH FUCK ARE YOUU")
            try:
                for model, data_list in zip([Contact, Country, Resource, Building], [iv, it, ir, ib]):
                    db.session.query(model).filter_by(currUserName=currUserName).delete()
                    for data in data_list:
                        item = model(**data)
                        db.session.add(item)
                db.session.query(CurrentlyBuildingNeedWork).filter_by(currUserName=currUserName).delete()
                db.session.query(CurrentlyBuilding).filter_by(currUserName=currUserName).delete()

                db.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                db.session.rollback()
def add_user(name, password, currUserName):
    max_id = db.session.query(func.max(user.id)).scalar()
    if max_id is None:
        max_id = -1  

    new_id = max_id + 1
    
    new_user = user(name=name, id=new_id, password=password, currUserName=currUserName)
    db.session.add(new_user)
    db.session.commit()

@app.route("/contacts/<string:currUserName>", methods=["GET"])
def get_contacts(currUserName):  
    contacts = Contact.query.filter(Contact.currUserName == currUserName).all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contacts/<string:currUserName>", methods=["POST"])
def create_contact(currUserName):
    value =  request.json.get("value")
    maximum = request.json.get("maximum")
    minimum = request.json.get("minimum")
    new_contact = Contact(value=value, maximum=maximum, minimum=minimum)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}),400
    return jsonify({"message": "USER CREATED!"}), 201



@app.route("/update_contact/<int:user_id>/<string:currUserName>", methods=["PATCH"])
def update_contact(currUserName,user_id):
    offset = user.query.get(currUserName).id
    contact = Contact.query.get(user_id + offset*contactOffset)
    if not contact:
        return jsonify({"message":  "NOT FOUND "}), 404
    modifier = 1
    data = request.json
    if contact.type == "JOB":
        og = contact.value
        modifier = Contact.query.get(14 + offset*contactOffset).value
    toAdd = data.get("value", 0) * modifier
    contact.maximum +=  data.get("maximum", 0)
    contact.minimum += data.get("minimum", 0)
    checking = contact.value
    contact.value +=  toAdd
    if contact.value < contact.minimum:
        contact.value = contact.minimum
        toAdd = checking-contact.minimum
    if contact.value > contact.maximum:
        contact.value = contact.maximum
    actualChange = contact.value - og
    addBack = 0
    if contact.type == "JOB":
        second = Contact.query.get(6 + offset*contactOffset)
        second.value -= actualChange
        if second.value < second.minimum:
            addBack = second.value - second.minimum
            second.value = second.minimum
        db.session.add(second) 
    contact.value += addBack

    db.session.commit()
    return jsonify({"message": " Values updated"}), 201  

@app.route("/set_contact/<int:user_id>/<string:currUserName>", methods=["PATCH"])
def set_contact(currUserName,user_id):
    try:
        offset = user.query.get(currUserName).id
        contact = Contact.query.get(user_id + offset*contactOffset)
        if not contact:
            return jsonify({"message":  "NOT FOUND "}), 404

        data = request.json
        contact.value =  data.get("value", 0)
        db.session.commit()
        return jsonify({"message": " Values updated"}), 201

    except  Exception as e:
        db.session.rollback()
        return jsonify({"message": "COULD NOT SET CONTACT", "error": str(e)}), 500




@app.route('/reset/<string:currUserName>', methods=['PATCH'])
def reset(currUserName):
    print(" RESETTTING ")
    data = request.json
    print("DATA   ", data)
    seeder = data['newV']
    print("seeder ", seeder)
    print(data['userName'])
    if request.method == 'PATCH':
            # db.session.query.filter(Contact.currUserName == currUserName).delete()
            # db.session.query(Resource).delete()
            # db.session.query(CurrentlyBuilding).delete()
            # db.session.query(Building).delete()
            # db.session.query(CurrentlyBuildingNeedWork).delete()
            # db.session.query(Country).delete()
            db.session.commit()
            seed_database(data['userName'], seeder)
            
            return jsonify({'message': 'Contacts reset successfully'}), 200

 
@app.route("/contacts/<int:user_id>/<string:currUserName>", methods=["GET"])
def getValue(currUserName,user_id):
    ##### add offset. add offset to everything ig
    offset = user.query.get(currUserName).id
    newId = user_id + offset * contactOffset
    #
    contact = Contact.query.get(newId)

    #contact = Contact.query.filter_by(id=newId, currUserName = currUserName).first()  #
    if not contact:
        return jsonify({"message": "Contact not found :(()"}), 404
    # Return just the 'value' attribute of the contact as JSON
    return jsonify({"value": contact.value})


@app.route("/contact/<int:user_id>/<string:currUserName>", methods=["GET"])
def getContact(currUserName,user_id):
    offset = user.query.get(currUserName).id
    newId = user_id + offset * contactOffset
   # contact = Contact.query.filter_by(id=newId,  currUserName = currUserName).first()  #
    contact = Contact.query.get(newId)
    if not contact:
        return jsonify({"message": "Contact not found :("}), 404
    # Return just the 'value' attribute of the contact as JSON
    return jsonify(contact.to_json())



def roundResources(currUserName):
    resources = Resource.query.filter(Resource.currUserName == currUserName).all()
    for resource in resources:
        resource.value = round(resource.value,3)
    db.session.commit()

##################################Resource functions
@app.route("/resources/<string:currUserName>", methods=["GET"]) 
def get_resources(currUserName):
    print("going to round  ", currUserName)
    roundResources(currUserName)                    ####################################important
    resources = Resource.query.filter(Resource.currUserName == currUserName).all()
    json_resources = list(map(lambda x: x.to_json(), resources))
    return jsonify({"resources": json_resources})

@app.route("/resources/<int:user_id>/<string:currUserName>", methods=["GET"])
def getValue2(currUserName,user_id):
    contact = Resource.query.filter_by(id=user_id, currUserName = currUserName).first()  
    offset = user.query.get(currUserName).id
    newId = user_id + offset * resourceOffset
    contact = Resource.query.get(newId)
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return jsonify({"value": contact.value})



@app.route("/update_resources/<int:user_id>/<string:currUserName>", methods=["PATCH"])
def update_resource(currUserName,user_id):
    offset = user.query.get(currUserName).id
    resource = Resource.query.get(user_id + offset*resourceOffset)
    if not resource:
        return jsonify({"message":  "NOT FOUND "}), 404

    data = request.json
    toAdd = data.get("value", 0)

    checking = resource.value
    resource.value +=  toAdd

    db.session.commit()
    return jsonify({"message": " Values updated"}), 201    

@app.route("/set_resources/<int:user_id>/<string:currUserName>", methods=["PATCH"])
def set_resource(currUserName,user_id):
    offset = user.query.get(currUserName).id
    resource = Resource.query.get(user_id + offset*resourceOffset)
    if not resource:
        return jsonify({"message":  "NOT FOUND "}), 404

    data = request.json
    resource.value = data.get("value", 0)

@app.route("/clearJobs/<string:currUserName>", methods = ["PATCH"]) 
def clearJobs(currUserName):
    offset = user.query.get(currUserName).id
    jobs = Contact.query.filter(Contact.currUserName == currUserName).all()
    addBack = 0
    for job in jobs:
        if job.type == "JOB":
            addBack += job.value
            job.value = 0
    avaliable = Contact.query.get(6 + offset*contactOffset)
    avaliable.value += addBack
    db.session.commit()

    return jsonify({"message": " Cleared :) "}), 201

@app.route("/buildings/<string:currUserName>", methods=["GET"]) 
def get_buildings(currUserName):
    #round perhaps?
    print("currUserName  ", currUserName)
    build = Building.query.filter(Building.currUserName == currUserName).all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/buildings/<int:user_id>/<string:currUserName>", methods=["GET"]) 
def getBuilding(currUserName,user_id):
    #round perhaps?
    offset = user.query.get(currUserName).id
    newId = user_id + offset * buildingOffset
    building = Building.query.get(newId)
    if not building:
        return jsonify({"message": "Contact not found"}), 404
    # Return just the 'value' attribute of the contact as JSON
    json_building = building.to_json() # (map(lambda x: x.to_json(), build2))

    z = jsonify({"buildingInfo": json_building})
    return z 


@app.route("/currently_building/<string:currUserName>", methods=["GET"]) 
def get_Currbuildings(currUserName):
    build = CurrentlyBuilding.query.filter(CurrentlyBuilding.currUserName == currUserName).all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/currently_building2/<string:currUserName>", methods=["GET"]) 
def get_Currbuildings2(currUserName):
    build = CurrentlyBuildingNeedWork.query.filter(CurrentlyBuildingNeedWork.currUserName == currUserName).all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/addCurr/<string:currUserName>", methods=["POST"])
def addCurrBuildings(currUserName):
    data = request.json 
    print(" SENDING THIS BACK  ", data)
    if not isinstance(data, list):
        return jsonify({"message": "Invalid input, expected a list of items"}), 400
    for item in data:
        value = item.get("value")
        name = item.get("name")
        if value is None or name is None: 
            return jsonify({"message": "Missing value or name in request data"}), 400
        print("ID  ", name)
        if item.get("level") is not None and CurrentlyBuilding.query.filter_by(name=name,  currUserName = currUserName).first():
            print("bad")
        else: 
            dbSize = db.session.query(CurrentlyBuilding).filter_by(currUserName=currUserName).count()
            if dbSize  > 0:
                above = CurrentlyBuilding.query.get(dbSize)
                print(above.value, " ", above.id, " ", above.name)
                if (str(name) == str(above.name)):
                    print("SAME SAME SAME SAME")
                    above.value += value
                    db.session.add(above)
                else :
                    print("DIFFERENT DIFFERENT DIFFERENT DIFFERENT  ", type(name) , "  ",  type(above.name))
                    new_contact = CurrentlyBuilding(value=value, name=name, currUserName=currUserName)
                    db.session.add(new_contact)

            else:
                new_contact = CurrentlyBuilding(value=value, name=name, currUserName=currUserName)
                db.session.add(new_contact)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()  
                return jsonify({"message": str(e)}), 400
        
    return jsonify({"message": "Buildings added successfully"}), 201

@app.route("/currentContent/<string:currUserName>", methods=["GET"])
def returnCurrentBuildings(currUserName):
    build = CurrentlyBuilding.query.filter(CurrentlyBuilding.currUserName == currUserName).all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    activeB = CurrentlyBuildingNeedWork.query.all()
    json_buildings += list(map(lambda x: x.to_json(), activeB))

    build2 = Building.query.filter(Building.currUserName == currUserName).all()
    json_buildings2 = list(map(lambda x: x.to_json(), build2))

    return jsonify({"buildings": json_buildings,"buildingList": json_buildings2})

@app.route("/hoverString/<string:type>/<string:currUserName>",methods=['GET'])
def returnHoverString(currUserName,type):
    return jsonify({"string" : hover.hoverString(type,currUserName)})


@app.route("/backEndSetUp/<string:currUserName>", methods=['PATCH'])
def backEndSetUp(currUserName):
    print("BACK END SET UP ,                                    DO YOU EVER ACTUALY DO THIS ", currUserName)
 
    return jsonify({"message": " Back end set up"}), 201   
import random
@app.route("/update_building/<int:user_id>/<string:currUserName>", methods=["PATCH"])
def update_building(currUserName,user_id):
    offset = user.query.get(currUserName).id
    building = Building.query.get(user_id + offset*buildingOffset)
    if not building:
         return jsonify({"message":  "NOT FOUND "}), 404
    modifier = Contact.query.get(14 + offset*contactOffset).value
    data = request.json
    toAdd = data.get("value", 0) * modifier
    og = building.working['value']
    newValue = og
    building.working['maximum'] +=  data.get("maximum", 0)
    building.working['minimum'] += data.get("minimum", 0)
    checking = newValue
    newValue +=  toAdd
    if newValue < building.working['minimum']:
        newValue = building.working['minimum']
        toAdd = checking-building.working['minimum']
    if newValue > building.working['maximum']:
        newValue = building.working['maximum']
    actualChange = newValue - og
    addBack = 0

    second = Contact.query.get(6 + offset*contactOffset)
    second.value -= actualChange
    if second.value < second.minimum:
        addBack = second.value - second.minimum
        second.value = second.minimum
        db.session.add(second) 
    newValue += addBack
### VALUE SHOWS TO BE UPDATED VALUE RIGHT HERE CORRECT
    max = building.working['maximum']
    building.working = None
    building.working = {'value': newValue, 'maximum': int(max), 'minimum': 0}
    db.session.add(building)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    return jsonify({"message": "Simple update test successful"}), 201

@app.route("/countryInnerString/<string:currUserName>",  methods=["GET"])
def countryInnerString(currUserName):
    string = country.countryInnerString(currUserName)
    return jsonify({"string" : string})

@app.route("/countryInnerStringNative/<string:currUserName>",  methods=["GET"])
def countryInnerStringNative(currUserName):
    string = country.countryInnerStringNative(currUserName)
    return jsonify({"string" : string})

@app.route("/factoryTab/<string:currUserName>",  methods=["GET"])
def factoryTabString(currUserName):
    string = buildings.factoryString(currUserName)
    return jsonify({"string" : string})

@app.route("/activeSupplyType/<string:currUserName>", methods=["PATCH"])
def activeSupplyType(currUserName):
    offset = user.query.get(currUserName).id
    data = request.json
    print("ACTIVE SUPPLY TYPE", data['activeSupplyType'] )
    supplyType = Contact.query.get(21 + offset*contactOffset)
    if data['activeSupplyType'] == 'resourceSupply':
        supplyType.value = 3
    elif data['activeSupplyType'] == 'toolSupply':
        supplyType.value = 2
    else:
        supplyType.value = 1
    time  = Contact.query.get(19 + offset*contactOffset)
    given = Contact.query.get(20 + offset*contactOffset)
    timeleft = time.efficiency.get(str(given.value), 50)
    time.value = timeleft
    db.session.add(time)
    db.session.commit()
    return jsonify({"message": "Simple update test successful"}), 201

@app.route("/countries/<string:currUserName>", methods=["GET"])
def get_countries(currUserName):  
    Countries = Country.query.filter(Contact.currUserName == currUserName).all()
    json_contacts = list(map(lambda x: x.to_json(), Countries))
    return jsonify({"Countries": json_contacts})

@app.route("/trade/<string:currUserName>", methods=["PATCH"])
def trade(currUserName):
    data = request.json
    country.trade(data, currUserName)
    return jsonify({"message": "Simple update test successful"}), 201

if __name__ == "__main__": ##### MUST BE AT BOTTOM
    with app.app_context():
        db.create_all() # creates all of the models
    app.run(debug=True)