from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork

def countryInnerString():
    townHall = Building.query.get(2)
    townHallLevel = townHall.value if townHall else 0
    string =  '<div class="TopLine"></div><h5 class="countryTitle" id="England">England - our overlord </h5>'
    print(" THL   ", townHallLevel)
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
            supplyShipsGiven = Contact.query.get(20).value
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
            



supplyShipIns = {0 :  { 'resourceSupply' : {'19' : 20, '6' : 5, '7' : 5, '9' : 5, '17':2, '18':2, '10' : 2, '11' : 2, '12' : 2, '13':1,'14':2,'15':3,'16':4},  'peopleSupply' : {'19' : 50, '6' : 1, '7' : 1, '9' : 1, '10' : 1, '11' : 1, '12' : 1, '14':2,'15':2,'16':2}, 'toolSupply': {'19' : 20, '6' : 1, '7' : 1, '9' : 2, '10' : 4, '11' : 4, '12' : 4, '13':6,'14':4,'15':5,'16':5}}}

def supplyString(typee):
    string = ''
    string += supplyStringFlesh(typee)
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string
def supplyStringFlesh(typee):
    supplyShipsGiven = Contact.query.get(20).value
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
    else:
        print(" NO SUPPLY SHIPS TO GIVE") 
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