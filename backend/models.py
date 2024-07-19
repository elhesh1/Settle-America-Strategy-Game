from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # first name
    # last name
    # email
    value = db.Column(db.Integer, unique=False, nullable=False) 
    maximum = db.Column(db.Integer, unique=False, nullable=True)
    minimum = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String, unique=True, nullable=True)
    type = db.Column(db.String, unique=False, nullable=True)
    def to_json(self):
        return {
            "id": self.id,
            "value" : self.value,
            "maximum" : self.maximum,
            "minimum" : self.minimum,
            "name" : self.name,
            "type" : self.type
        }  