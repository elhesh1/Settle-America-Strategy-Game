# does some CRUD shit
# GET - Get somethin
# POST - Post something (idk if we Ill need it)
# PATCH - update ---

# Request returns a Response. status:200 means success
from flask import request, jsonify
from config import app, db
from models import Contact, Resource

import random
from variableHelpers import initial_variables, initial_resources
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

    data = request.json
    toAdd = data.get("value", 0)
    contact.maximum +=  data.get("maximum", 0)
    contact.minimum += data.get("minimum", 0)
    checking = contact.value
    contact.value +=  toAdd
    if contact.value < contact.minimum:
        contact.value = contact.minimum
        toAdd = checking-contact.minimum
    if contact.value > contact.maximum:
        contact.value = contact.maximum

    addBack = 0
    if contact.type == "JOB":
        second = Contact.query.get(6)
        second.value -= toAdd
        if second.value < second.minimum:
            print("WE TOO HIGH")
            addBack = second.value - second.minimum
            second.value = second.minimum
        db.session.add(second)  
    contact.value += addBack


    print(4)
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
    print("a")
    print(initial_resources)

    for a in initial_resources:
        print("watermelon")
        b = Resource(**a)
        print(b)
        try:
            db.session.add(b)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  






@app.route('/reset', methods=['PATCH'])
def reset():
    if request.method == 'PATCH':
            db.session.query(Contact).delete()
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


##################################Resource functions
@app.route("/resources", methods=["GET"]) 
def get_resources():
    # print("BRUH GETTING RESOURCES NO CAP")
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








if __name__ == "__main__":
    with app.app_context():
        db.create_all() # creates all of the modesl
    app.run(debug=True)