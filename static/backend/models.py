

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, func

from static.backend.variableHelpers import initial_variables, initial_resources, initial_buildings, initial_countries
import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
contactOffset = len(initial_variables) 
resourceOffset = len(initial_resources) 
buildingOffset = len(initial_buildings) 
countryOffset = len(initial_countries) 
class user(db.Model):
    name = db.Column(db.String, primary_key=True)
    id = db.Column(db.Integer, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)
    currUserName = db.Column(db.String, nullable=False, unique=False) 
    def to_json(self):
        return {
            "name" : self.name,
            "password" : self.password,
            "currUserName" : self.currUserName,
            "id" : self.id
        }

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    maximum = db.Column(db.Integer, unique=False, nullable=False, default=2147483646)
    minimum = db.Column(db.Integer, unique=False, nullable=False, default=-2147483646)
    name = db.Column(db.String, unique=False, nullable=True)
    type = db.Column(db.String, unique=False, nullable=True)
    efficiency = db.Column(db.JSON, unique=False, nullable=True)
    currUserName = db.Column(db.String, nullable=False, unique=False)

    def to_json(self):
        return {
            "id": self.id,
            "value" : self.value,
            "maximum" : self.maximum,
            "minimum" : self.minimum,
            "name" : self.name,
            "type" : self.type,
            "efficiency" : self.efficiency,
            "currUserName" : self.currUserName
        }  
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    cook = db.Column(db.Integer, nullable=True, unique=False)
    name = db.Column(db.String, unique=False, nullable=True)
    integer = db.Column(db.Integer, unique=False, default=0)
    always = db.Column(db.Integer, unique=False, default=0)    
    currUserName = db.Column(db.String, nullable=False, unique=False)

    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "cook" : self.cook,
            "integer" : self.integer,
            "always" : self.always,
            "currUserName" : self.currUserName
        }
    
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    name = db.Column(db.String, unique=False, nullable=True)
    fullname = db.Column(db.String, unique=False, nullable=True)
    typeOfBuilding = db.Column(db.String, unique=False, nullable=True)
    work = db.Column(db.Integer, unique=False, nullable=False, default=0)
    cost = db.Column(db.JSON, nullable=True) 
    capacity = db.Column(db.Integer, unique=False, nullable=False, default=0)
    working  = db.Column(db.JSON, nullable=True)  
    tools = db.Column(db.JSON, nullable=True)
    Outputs = db.Column(db.JSON, nullable=True)
    Inputs =  db.Column(db.JSON, nullable=True)
    currUserName = db.Column(db.String, nullable=False, unique=False)
    def __init__(self, *args, **kwargs):
        super(Building, self).__init__(*args, **kwargs)
        if self.name and not self.fullname:
            self.fullname = self.name
        if not self.tools:
            self.tools = {"None" : 1, "With" : [1,0], "Base" : 0.1}
        if not self.Inputs:
            self.Inputs = {}
        if not self.Outputs:
            self.Outputs = {}
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "work" : self.work,
            "cost" : self.cost,
            "capacity" : self.capacity,
            "fullname" : self.fullname,
            "typeOfBuilding" : self.typeOfBuilding,
            "working" : self.working,
            "tools" : self.tools,
            "Inputs" : self.Inputs,
            "Outputs" : self.Outputs,
            "currUserName" : self.currUserName
            }
    
class CurrentlyBuilding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=True) 
    name = db.Column(db.Integer, unique=False, nullable=True)
    level = db.Column(db.Integer, unique=False, nullable=True)
    currUserName = db.Column(db.String, nullable=False, unique=False)
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "level" : self.level,
            "currUserName" : self.currUserName
            }
    
class CurrentlyBuildingNeedWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False) 
    name = db.Column(db.Integer, unique=False, nullable=True)
    type = db.Column(db.Integer, unique=False, nullable=True)
    currUserName = db.Column(db.String, nullable=False, unique=False)
    def to_json(self):
        return {
            "id" : self.id,
            "value" : self.value,
            "name" : self.name,
            "type" : "CURRENT",
            "currUserName" : self.currUserName
            }
    
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pop = db.Column(db.Integer, unique=False, nullable=False) 
    name = db.Column(db.String, unique=False, nullable=False)
    opinion = db.Column(db.Integer, unique=False, nullable=True)
    type = db.Column(db.String, unique=False, nullable=False, default='Native')
    trades = db.Column(db.JSON, nullable=True)
    currUserName = db.Column(db.String, nullable=False, unique=False)
    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "pop" : self.pop,
            "opinion" : self.opinion,
            "type" : self.type,
            "trades" : self.trades,
            "currUserName" : self.currUserName
            }
