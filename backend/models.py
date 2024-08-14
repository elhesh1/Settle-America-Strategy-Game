from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    maximum = db.Column(db.Integer, unique=False, nullable=True)
    minimum = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String, unique=True, nullable=True)
    type = db.Column(db.String, unique=False, nullable=True)
    efficiency = db.Column(db.JSON, unique=False, nullable=True)
    def to_json(self):
        return {
            "id": self.id,
            "value" : self.value,
            "maximum" : self.maximum,
            "minimum" : self.minimum,
            "name" : self.name,
            "type" : self.type,
            "efficiency" : self.efficiency
        }  
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    cook = db.Column(db.Integer, nullable=True, unique=False)
    name = db.Column(db.String, unique=True, nullable=True)
    integer = db.Column(db.Integer, unique=False, default=0)
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "cook" : self.cook,
            "integer" : self.integer
        }
    
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    name = db.Column(db.String, unique=True, nullable=True)
    fullname = db.Column(db.String, unique=True, nullable=True)
    typeOfBuilding = db.Column(db.String, unique=False, nullable=True)
    work = db.Column(db.Integer, unique=True, nullable=True)
    cost = db.Column(db.JSON, nullable=True) 
    capacity = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, *args, **kwargs):
        super(Building, self).__init__(*args, **kwargs)
        if self.name and not self.fullname:
            self.fullname = self.name

    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "work" : self.work,
            "cost" : self.cost,
            "capacity" : self.capacity,
            "fullname" : self.fullname,
            "typeOfBuilding" : self.typeOfBuilding
            }
    
class CurrentlyBuilding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=True) 
    name = db.Column(db.Integer, unique=False, nullable=True)
    level = db.Column(db.Integer, unique=False, nullable=True)
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "level" : self.level
            }
    
class CurrentlyBuildingNeedWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    name = db.Column(db.Integer, unique=False, nullable=True)
    type = db.Column(db.Integer, unique=False, nullable=True)
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "type" : "CURRENT"
            }