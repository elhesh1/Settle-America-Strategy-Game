# does some CRUD shit
# GET - Get somethin
# POST - Post something (idk if we Ill need it)
# PATCH - update ---

# Request returns a Response. status:200 means success
from flask import request, jsonify
from config import app, db
from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
import citizenActions
import random
import advance
from variableHelpers import initial_variables, initial_resources, initial_buildings
from sqlalchemy.exc import IntegrityError

@app.route("/contacts", methods=["GET"])
def get_contacts():  
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contacts", methods=["POST"])
def create_contact():
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



@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({"message":  "NOT FOUND "}), 404
    modifier = 1
    data = request.json
    if contact.type == "JOB":
        og = contact.value
        modifier = Contact.query.get(14).value
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
        second = Contact.query.get(6)
        second.value -= actualChange
        if second.value < second.minimum:
            addBack = second.value - second.minimum
            second.value = second.minimum
        db.session.add(second) 
    contact.value += addBack

    db.session.commit()
    return jsonify({"message": " Values updated"}), 201



def seed_database():
    for contact_data in initial_variables:
        contact = Contact(**contact_data)
        try:
            db.session.add(contact)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for a in initial_resources:
        b = Resource(**a)
        try:
            db.session.add(b)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  
    
    for a in initial_buildings:
        b = Building(**a)
        try:
            db.session.add(b)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()    

@app.route("/set_contact/<int:user_id>", methods=["PATCH"])
def set_contact(user_id):
    try:
        contact = Contact.query.get(user_id)
        if not contact:
            return jsonify({"message":  "NOT FOUND "}), 404

        data = request.json
        contact.value =  data.get("value", 0)
        db.session.commit()
        return jsonify({"message": " Values updated"}), 201

    except  Exception as e:
        db.session.rollback()
        return jsonify({"message": "COULD NOT SET CONTACT", "error": str(e)}), 500




@app.route('/reset', methods=['PATCH'])
def reset():
    if request.method == 'PATCH':
            db.session.query(Contact).delete()
            db.session.query(Resource).delete()
            db.session.query(CurrentlyBuilding).delete()
            db.session.query(Building).delete()
            db.session.query(CurrentlyBuildingNeedWork).delete()
            db.session.commit()
            seed_database()
            return jsonify({'message': 'Contacts reset successfully'}), 200


@app.route("/contacts/<int:user_id>", methods=["GET"])
def getValue(user_id):
    contact = Contact.query.filter_by(id=user_id).first()  #
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    # Return just the 'value' attribute of the contact as JSON
    return jsonify({"value": contact.value})

def roundResources():
    resources = Resource.query.all()
    for resource in resources:
        resource.value = round(resource.value,3)
    db.session.commit()

##################################Resource functions
@app.route("/resources", methods=["GET"]) 
def get_resources():
    roundResources()                    ####################################important
    resources = Resource.query.all()
    json_resources = list(map(lambda x: x.to_json(), resources))
    return jsonify({"resources": json_resources})

@app.route("/resources/<int:user_id>", methods=["GET"])
def getValue2(user_id):
    contact = Resource.query.filter_by(id=user_id).first()  
    # # just copy and pasted contact thats why the naming is off
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return jsonify({"value": contact.value})



@app.route("/update_resources/<int:user_id>", methods=["PATCH"])
def update_resource(user_id):
    resource = Resource.query.get(user_id)
    if not resource:
        return jsonify({"message":  "NOT FOUND "}), 404

    data = request.json
    toAdd = data.get("value", 0)

    checking = resource.value
    resource.value +=  toAdd

    db.session.commit()
    return jsonify({"message": " Values updated"}), 201    

@app.route("/set_resources/<int:user_id>", methods=["PATCH"])
def set_resource(user_id):
    resource = Resource.query.get(user_id)
    if not resource:
        return jsonify({"message":  "NOT FOUND "}), 404

    data = request.json
    resource.value = data.get("value", 0)

@app.route("/clearJobs", methods = ["PATCH"]) 
def clearJobs():
    jobs = Contact.query.all()
    addBack = 0
    for job in jobs:
        if job.type == "JOB":
            addBack += job.value
            job.value = 0
    avaliable = Contact.query.get(6)
    avaliable.value += addBack
    db.session.commit()

    return jsonify({"message": " Cleared :) "}), 201

@app.route("/buildings", methods=["GET"]) 
def get_buildings():
    #round perhaps?
    build = Building.query.all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/buildings/<int:user_id>", methods=["GET"]) 
def getBuilding(user_id):
    #round perhaps?

    building = Building.query.filter_by(id=user_id).first()  #
    print('buildinggg,  ' , building )
    if not building:
        return jsonify({"message": "Contact not found"}), 404
    # Return just the 'value' attribute of the contact as JSON
    json_building = building.to_json() # (map(lambda x: x.to_json(), build2))
    z = jsonify({"buildingInfo": json_building})
    return z 


@app.route("/currently_building", methods=["GET"]) 
def get_Currbuildings():
    build = CurrentlyBuilding.query.all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/currently_building2", methods=["GET"]) 
def get_Currbuildings2():
    build = CurrentlyBuildingNeedWork.query.all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    return jsonify({"buildings": json_buildings})

@app.route("/addCurr", methods=["POST"])
def addCurrBuildings():
    data = request.json 
    if not isinstance(data, list):
        return jsonify({"message": "Invalid input, expected a list of items"}), 400
    for item in data:
        value = item.get("value")
        name = item.get("name")
        if value is None or name is None:
            return jsonify({"message": "Missing value or name in request data"}), 400
        dbSize = db.session.query(CurrentlyBuilding).count()
        if dbSize  > 0:
            above = CurrentlyBuilding.query.get(dbSize)
            print(above.value, " ", above.id, " ", above.name)
            if (str(name) == str(above.name)):
                print("SAME SAME SAME SAME")
                above.value += value
                db.session.add(above)
            else :
                print("DIFFERENT DIFFERENT DIFFERENT DIFFERENT  ", type(name) , "  ",  type(above.name))
                new_contact = CurrentlyBuilding(value=value, name=name)
                db.session.add(new_contact)

        else:
            new_contact = CurrentlyBuilding(value=value, name=name)
            db.session.add(new_contact)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  
            return jsonify({"message": str(e)}), 400
    return jsonify({"message": "Buildings added successfully"}), 201

@app.route("/currentContent", methods=["GET"])
def returnCurrentBuildings():
    build = CurrentlyBuilding.query.all()
    json_buildings = list(map(lambda x: x.to_json(), build))
    activeB = CurrentlyBuildingNeedWork.query.all()
    json_buildings += list(map(lambda x: x.to_json(), activeB))

    build2 = Building.query.all()
    json_buildings2 = list(map(lambda x: x.to_json(), build2))

    return jsonify({"buildings": json_buildings,"buildingList": json_buildings2})


if __name__ == "__main__": ##### MUST BE AT BOTTOM
    with app.app_context():
        db.create_all() # creates all of the modesl
    app.run(debug=True)