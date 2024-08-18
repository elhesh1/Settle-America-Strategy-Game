from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork

def countryInnerString():
    townHallLevel = Building.query.get(2).value

    string =  '<div class="TopLine"></div><h5 class="countryTitle" id="England">England - our overlord </h5>'

    if townHallLevel == 0:
       string += '<h3 class="countryExplanation" id="EnglandExplanation">Since our settlement does not have a town hall, the English are refusing to send us any people or funds</h3>'
    elif townHallLevel > 0:
        string +='<h3 class="countryExplanation" id="EnglandExplanation">Next supply ship: '+ str(Contact.query.get(19).value) + ' weeks </h3>'
    else:
        string +='<h3 class="countryExplanation" id="EnglandExplanation">Broken or not implemented yet: </h3>'

    return string

def advance():
    if Building.query.get(2).value > 0:
        timeUntil = Contact.query.get(19)
        timeUntil.value -= 1