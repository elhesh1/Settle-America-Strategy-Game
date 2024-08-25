from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, Country
import re
from config import app, db
from variableHelpers import factoryTrades

def countryInnerString():
    string = '<div class="country-flex-container" id="country-flex-England"><div class="countryTitleRow" id="countryGridEngland">'
    townHall = Building.query.get(2)
    townHallLevel = townHall.value if townHall else 0
    string +=  '<div class="TopLine"></div><h5 class="countryTitle" id="England">England - our overlord </h5>'
    if townHallLevel == 0:
       string += '<h3 class="countryExplanation" id="EnglandExplanation">Since our settlement does not have a town hall, the English are refusing to send us any people or funds</h3>'
    elif townHallLevel > 0:
        supplyTime = Contact.query.get(19).value
        if supplyTime < 1:
            string +='<h3 class="countryExplanation" id="EnglandExplanation">Request supply ship:  </h3>'
            string += '<button class="requestSupply" id="peopleSupply">People</button>'
            string += '<button class="requestSupply" id="toolSupply">Tools</button>'  
            string += '<button class="requestSupply" id="resourceSupply">Resources</button>'

        else: 
            string +='<h3 class="countryExplanation HoverSupply" id="EnglandExplanation">Time until supply ship: '+ str(Contact.query.get(19).value) + ' weeks </h3>'
    else:
        string +='<h3 class="countryExplanation" id="EnglandExplanation">Broken or not implemented yet: </h3>'
    string += '</div></div>'
    return string

def countryInnerStringNative():
    natives = Country.query.all()
    string = ""
    for native in natives:
        if native.type == 'Native':
            cName = native.name
            string +=  '<div class="country-flex-container" id="country-flex-'+ cName + '"><div class="countryTitleRow" id="countryGrid'+ cName + '">'
            townHall = Building.query.get(2)
            townHallLevel = townHall.value if townHall else 0
            string +=  '<div class="TopLine"></div><h5 class="countryTitle" id="'+ cName + '">'+ cName + ' - native tribe </h5>'
            if native.trades:
                string += '<div class="TradeBox">'
                string += '<div class="InnerTradeGrid">' 
                string +='<h3 class="giveTrade" style="text-decoration: underline;">Give</h3>'
                string += '<span class=arrowTrade>&#8594;</span>'
                string +='<h3 class="getTrade"   style="text-decoration: underline;">Receive</h3>' 
                string +=  '</div>'
                number = 0
                for trade in native.trades:
                    number += 1
                    string += '<div class="InnerTradeGrid">'        
                    string +='<h3 class="giveTrade"">' +  str(trade[1]) + ' ' + str(Resource.query.get(trade[0]).name)  + '</h3>'
                    string += '<span class=arrowTrade>&#8594;</span>'
                    string +='<h3 class="getTrade"">' + str(trade[3])  + ' ' +  str(Resource.query.get(trade[2]).name) +   '</h3>'
                    string += '<button class="TradeButton" id="TradeButton' + cName + str(number) + '" >Trade</button>'
                    string +=  '</div>'
                string += '</div></div>'
            string +=  '</div>'
            
        string += '</div>'

    return string

def advance():
    if Building.query.get(2).value > 0:
        timeUntil = Contact.query.get(19)
        timeUntil.value -= 1
        if timeUntil.value == 0:        ####### gives you the supply stuff
            typeeNumber = Contact.query.get(21).value
            if typeeNumber == 3:
                typee = 'resourceSupply'
            elif typeeNumber == 2:
                typee = 'toolSupply'
            else:
                typee = 'peopleSupply'
            supplyShipsGiven = Building.query.get(2).value
            gives = supplyShipIns[supplyShipsGiven][typee]
            for key in gives:
                currentResource = Resource.query.get(key)
                currentResource.value += gives[key]
            people = Resource.query.get(19)
            population = Contact.query.get(5)
            population.value += people.value
            avaliable = Contact.query.get(6)
            avaliable.value += people.value
            people.value = 0
            



supplyShipIns = {0 :  { 'resourceSupply' : {'19' : 20, '6' : 5, '7' : 5, '9' : 5, '17':2, '18':2, '10' : 2, '11' : 2, '12' : 2, '13':1,'14':2,'15':3,'16':4},  'peopleSupply' : {'19' : 50, '6' : 1, '7' : 1, '9' : 1, '10' : 1, '11' : 1, '12' : 1, '14':2,'15':2,'16':2}, 'toolSupply': {'19' : 20, '6' : 1, '7' : 1, '9' : 2, '10' : 4, '11' : 4, '12' : 4, '13':6,'14':4,'15':5,'16':5}},
                 1 : { 'resourceSupply' : {'19' : 40, '6' : 8, '7' : 8, '9' : 8, '17':4, '18':4, '10' : 4, '11' : 4, '12' : 4, '13':2,'14':4,'15':5,'16':6},  'peopleSupply' : {'19' : 100, '6' : 2, '7' : 2, '9' : 2, '10' : 2, '11' : 2, '12' : 3, '14':3,'15':3,'16':3}, 'toolSupply': {'19' : 40, '6' : 2, '7' : 2, '9' : 4, '10' : 8, '11' : 6, '12' : 8, '13':10,'14':8,'15':10,'16':12}}}

def supplyString(typee):
    string = ''
    string += supplyStringFlesh(typee)
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string
def supplyStringFlesh(typee):
    supplyShipsGiven = Building.query.get(2).value - 1
    string = ''
    if supplyShipsGiven in supplyShipIns:
        gives = supplyShipIns[supplyShipsGiven][typee]
        for key in gives:
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += str(Resource.query.get(key).name)
                    string += '</div> <div style="text-align: right;">'
                    string += str(gives[key])
                    string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    return string



def supplyToolTip():
    typeeNumber = Contact.query.get(21).value
    if typeeNumber == 3:
         typee = 'resourceSupply'
    elif typeeNumber == 2:
         typee = 'toolSupply'
    else:
         typee = 'peopleSupply'
    string = ''
    string += supplyStringFlesh(typee)
    
    return string
def split_string(data):
    letters = ''.join(re.findall(r'[a-zA-Z]', data))
    numbers = ''.join(re.findall(r'[0-9]', data))
    return letters, int(numbers)


def trade(data):
    print(" TRADEING ", data)
    name, number = split_string(data['buttonName'])
    if name == 'FactoryButton':
        print()
        input = Resource.query.get(factoryTrades[number][0])
        output = Resource.query.get(factoryTrades[number][2])
        if input.value >= float(factoryTrades[number][1]):
            input.value -= factoryTrades[number][1]
            output.value += factoryTrades[number][3]
            db.session.commit()
    else:
        country = Country.query.filter_by(name=name.capitalize()).first()
        trade = country.trades[int(number)-1]
        input = Resource.query.get(trade[0])
        output = Resource.query.get(trade[2])
        if input.value >= float(trade[1]):
            input.value -= trade[1]
            output.value += trade[3]
            db.session.commit()

