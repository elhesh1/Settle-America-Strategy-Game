import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, user,contactOffset,resourceOffset,buildingOffset,countryOffset
from flask import request, jsonify
from static.backend.variableHelpers import initial_variables
import static.backend.advance
import static.backend.hover as hover
import static.backend.buildings as buildings

nFoodTypes = 0 
# .filter(Contact.currUserName == currUserName)
def eat(currUserName):
    offset = user.query.get(currUserName).id
    global foodTypes
    rationingPval = Contact.query.get(12 + offset*contactOffset).value
    expectedFood = rationingPval * 0.01 * Contact.query.get(5 + offset*contactOffset).value * 0.02 
    eatHelper(expectedFood,currUserName)
    if  Contact.query.get(5 + offset*contactOffset).value != 0:
        housedRatio  = Building.query.get(1 + offset*buildingOffset).value * Building.query.get(1 + offset*buildingOffset).capacity / Contact.query.get(5 + offset*contactOffset).value # may want to change this one as well
        if housedRatio > 1:
            housedRatio = 1
    else:
        housedRatio = 0 
    season = Contact.query.get(8 + offset*contactOffset)
    if season.value == 1:
        housedValue = 0.85 + 0.15*housedRatio
    elif season.value == 2:
        housedValue = 0.9 + 0.1*housedRatio
    elif season.value == 3:
        housedValue = 0.85 + 0.15*housedRatio
    else:
        housedValue = 0.1 + 0.9*housedRatio
    if nFoodTypes == 0:         ### you are starving 
        rationingPval = 15 # basically the minimum if you can't eat
    HealthEquilibrium = rationingPval *0.01 * (68+nFoodTypes*8) * housedValue
    HealthCurrent = Contact.query.get(13 + offset*contactOffset)
    NumberFoodTypes = Contact.query.get(17 + offset*contactOffset)
    NumberFoodTypes.value = nFoodTypes

    HealthCurrent.value = round(HealthEquilibrium,0)

    db.session.commit()

    return jsonify({"message": " Values updated"}), 201

def eatHelper(expectedFood,currUserName):
    offset = user.query.get(currUserName).id
    global nFoodTypes
    FoodTypeValues = [0,0,0,0]
    nFoodTypes = 0
    # fruits, vegtables, meat, grain        
    FoodTypeValues[0] = Resource.query.get(8 + offset*resourceOffset).value
    FoodTypeValues[1] = Resource.query.get(9 + offset*resourceOffset).value
    FoodTypeValues[2] = Resource.query.get(7 + offset*resourceOffset).value
    FoodTypeValues[3] = Resource.query.get(6 + offset*resourceOffset).value
                       # Only did one food for each value needs to be updated in the futrere/////////////////////
    foodmin = 9999999
    for FoodVal in FoodTypeValues:
        if FoodVal > 0:
            nFoodTypes += 1
            if FoodVal < foodmin:
                foodmin = FoodVal
    if nFoodTypes == 0:
        return 
    if foodmin >= expectedFood/nFoodTypes:
        change = expectedFood/nFoodTypes
        val8  = Resource.query.get(8 + offset*resourceOffset)
        val7 = Resource.query.get(7 + offset*resourceOffset)
        val6 = Resource.query.get(6 + offset*resourceOffset)
        val9 = Resource.query.get(9 + offset*resourceOffset)
        val8.value -= change
        val9.value -= change
        val7.value -= change
        val6.value -= change
        if val8.value < 0:
            val8.value = 0
        if val9.value < 0:
            val9.value = 0
        if val7.value < 0:
            val7.value = 0
        if val6.value < 0:
            val6.value = 0
         
    else :
        change = foodmin
        foodleft = expectedFood - foodmin*4
        nFoodTypes -= 0.75 ##################### could change this if you are up for it some day
        val8  = Resource.query.get(8 + offset*resourceOffset)
        val7 = Resource.query.get(7 + offset*resourceOffset)
        val6 = Resource.query.get(6 + offset*resourceOffset)
        val9 = Resource.query.get(9 + offset*resourceOffset)
        val8.value -= change
        val9.value -= change
        val7.value -= change
        val6.value -= change
        if val8.value < 0:
            val8.value = 0
            foodleft += foodmin 
        if val9.value < 0:
            val9.value = 0
            foodleft += foodmin
        if val7.value < 0:
            val7.value = 0
            foodleft += foodmin
        if val6.value < 0:
            val6.value = 0
            foodleft += foodmin
        db.session.commit()
        eatHelper(foodleft,currUserName)

    db.session.commit()

def build(currUserName): #16
    offset = user.query.get(currUserName).id
    global weeklyBuildPower
    global buildingsBuiltThisWeek
    buildingsBuiltThisWeek = {}
    weeklyBuildPower = BuilderEff(currUserName)[2] 
    index = Contact.query.get(16 + offset*contactOffset).value - 1
    current = CurrentlyBuilding.query.filter(CurrentlyBuilding.currUserName == currUserName).all()
    for i in range(index, len(current)):        # iterate through each building
        c = current[i]
        print("CURRENTLY BUILDING : " , current)
        buildbuild(c,i,currUserName)
    rows = CurrentlyBuilding.query.filter(Resource.currUserName == currUserName).all()
    for row in rows:
        if row.value == 0:
            db.session.delete(row)  
    db.session.commit()
    buildings.reactToBuildings(buildingsBuiltThisWeek,currUserName)


def buildbuild(c,i,currUserName):
    offset = user.query.get(currUserName).id
    global weeklyBuildPower
    global buildingsBuiltThisWeek
    temp = c.name
    ### IF the building in the queue is too low check the top. Maybe make it so each building can only "see" its type
    if  CurrentlyBuildingNeedWork.query.filter_by(name=temp,  currUserName = currUserName).first() is None:
        print(" c:  ", c, " ", temp)
        if c.value > 0:             
            print("C C C C C ", c )
            building = Building.query.get(c.name)   ## dont add offset, its already been calculated
            if c.name == 2 or c.name == 7:
                print("update?")
                building = Building.query.get(c.name + offset*buildingOffset)   ## this is for leveled buildings, its wierd ik

            print("BUILDING COST  " , building.cost)
            cost = building.cost
            work = building.work
            print("BL ", building.value)
            if (cost == -1):
                cost = hover.buildingLevels[building.value+1]['cost']     # make a call to the level table #######################################
            if (work == -1):
                work = hover.buildingLevels[building.value+1]['work']  # make a call the correct table dufus
            print(" COST ", type(cost), "  ", cost, "really doe")


            good = 0
            for key in cost:                       # iterate through each building requeremint
                resource = Resource.query.get(int(key) + offset*resourceOffset)  # '5'
                costA = cost[key]
                if  costA > resource.value:
                    good = 1
                else:
                    resource.value -= costA
                    db.session.add(resource)
            if good == 0:
                c.value -= 1
                c.value = round(c.value,0) ### this should be added to ACTIVE. then use up builders. Maybe have an active queue as
                print("HAVE RESOURCES TO BUILD ... ", c )
                db.session.commit()
                if work <= weeklyBuildPower: # we have enough power to build it this week 
                    print("ENOUGH POWER TO BUILD ", work, " ", weeklyBuildPower)
                    weeklyBuildPower -= work
                    building.value += 1
                    ###################################### built
                    buildingsBuiltThisWeek[building.id] = 1
                    db.session.commit()
                    buildbuild(c,i,currUserName)
                else:
                    c.value += 1
                    c.value = round(c.value,0)
                    print( "NOT ENOUGH POWER :(", work, " ", weeklyBuildPower)
                    currentBuilding = CurrentlyBuildingNeedWork(name = building.id , value = work-weeklyBuildPower , currUserName = currUserName)
                    weeklyBuildPower = 0
                    db.session.add(currentBuilding)
                    db.session.commit()
        else:
            db.session.rollback()
    else:
        CurrentlyBuildingNeedsMoreWork = CurrentlyBuildingNeedWork.query.filter_by(name=temp,  currUserName = currUserName).first()
        print("YOU ALREADY GOT SOME SHIT IN THERE")
        if CurrentlyBuildingNeedsMoreWork.value > weeklyBuildPower:
            CurrentlyBuildingNeedsMoreWork.value -= weeklyBuildPower
            weeklyBuildPower = 0 
            db.session.add(CurrentlyBuildingNeedsMoreWork)
            db.session.commit()
        else:
            weeklyBuildPower -= CurrentlyBuildingNeedsMoreWork.value
            buildingType = Building.query.get(CurrentlyBuildingNeedsMoreWork.name) # no offset
            buildingType.value += 1
            print("BULIDNG TYPE FR ::::::: ", buildingType.name, " ")
            newC = CurrentlyBuilding.query.filter_by(name=CurrentlyBuildingNeedsMoreWork.name,  currUserName = currUserName).first()
            newC.value -= 1
            newC.value = round(newC.value,0)
           # db.session.query(CurrentlyBuildingNeedWork).delete()
            print(" FINISHED>>> ", CurrentlyBuildingNeedsMoreWork.name)
            db.session.query(CurrentlyBuildingNeedWork).filter_by(name=CurrentlyBuildingNeedsMoreWork.name,  currUserName = currUserName).delete()
            db.session.add(buildingType)
            buildingsBuiltThisWeek[buildingType.id] = 1
            #################################################
            db.session.commit()
            buildbuild(c,i,currUserName)

def farmerEff(season,currUserName):
        offset = user.query.get(currUserName).id
        JobValue = Contact.query.get(hover.jobMap['farmer'] + offset*contactOffset)
        baseEfficiency = JobValue.efficiency['e']
        strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
        Season = str(Contact.query.get(8 + offset*contactOffset).value)
        seasonEfficiency = JobValue.efficiency['season'][Season]
        count = int(JobValue.value)
        if int(season) == 1:
            IronHoeMax = int(Resource.query.get(10 + offset*resourceOffset).value)
            IronHoeEfficiency = 1
            NoToolEfficiency = 0.5 
            if IronHoeMax >= count:
                UsingIronHoe = count
            else:
                UsingIronHoe = IronHoeMax
            UsingNoTools = int(count - UsingIronHoe)
            if count != 0:
                totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronHoeEfficiency * UsingIronHoe)+(NoToolEfficiency*UsingNoTools)) / count )
            else:
                totalEfficiency = baseEfficiency * seasonEfficiency * IronHoeEfficiency * strength
            return count * totalEfficiency, IronHoeEfficiency, UsingIronHoe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Iron Hoe', 'Planted'
        elif int(season) == 3: 
            IronSickleMax = int(Resource.query.get(11 + offset*resourceOffset).value)
            IronSickleEfficiency = 1
            NoToolEfficiency = 0.5 
            if IronSickleMax >= count:
                UsingIronSickle = count
            else:
                UsingIronSickle = IronSickleMax
            UsingNoTools = int(count - UsingIronSickle)
            if count != 0:
                totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronSickleEfficiency * UsingIronSickle)+(NoToolEfficiency*UsingNoTools)) / count )
            else:
                totalEfficiency = baseEfficiency * seasonEfficiency * IronSickleEfficiency * strength
            return  count * totalEfficiency, IronSickleEfficiency, UsingIronSickle, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Iron Sickle', 'Harvested'
        else:
            NoToolEfficiency = 0.18
            UsingNoTools = count
            totalEfficiency =  NoToolEfficiency * baseEfficiency
            return count*totalEfficiency, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Berries Foraged' 


def LoggerEff(currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(hover.jobMap['logger'] + offset*contactOffset)
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
    Season = str(Contact.query.get(8 + offset*contactOffset).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    IronAxeMax = int(Resource.query.get(12 + offset*resourceOffset).value)
    IronAxeEfficiency = 1
    NoToolEfficiency = 0.5 
    if IronAxeMax >= count:
        UsingIronAxe = count
    else:
        UsingIronAxe = IronAxeMax
    UsingNoTools = int(count - UsingIronAxe)
    if count != 0:
        totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronAxeEfficiency * UsingIronAxe)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency * seasonEfficiency * IronAxeEfficiency * strength
    return IronAxeEfficiency, UsingIronAxe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, count * totalEfficiency

def HunterEff(currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(hover.jobMap['hunter'] + offset*contactOffset)
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
    Season = str(Contact.query.get(8 + offset*contactOffset).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    RifleMax = int(Resource.query.get(13 + offset*resourceOffset).value)
    BowMax = int(Resource.query.get(14 + offset*resourceOffset).value)
    RifleEfficiency = 1.5
    BowEfficiency = 1
    NoToolEfficiency = 0.5 
    UsingBow = 0
    if RifleMax >= count:
        UsingRifle = count
        UsingNoTools = int(count - UsingRifle)
    else:
        UsingRifle = RifleMax
        noRifle = int(count-UsingRifle)
        if BowMax >= noRifle:
            UsingBow = noRifle
            UsingNoTools = 0
        else:
            UsingBow = BowMax
            UsingNoTools = int(noRifle - BowMax)
    if count != 0:
        totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((RifleEfficiency * UsingRifle)+(BowEfficiency * UsingBow)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency * seasonEfficiency * RifleEfficiency * strength
    return RifleEfficiency, UsingRifle, BowEfficiency, UsingBow, NoToolEfficiency, UsingNoTools, count, totalEfficiency, count*totalEfficiency

def CooksEff(currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(hover.jobMap['cook'] + offset*contactOffset)
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
    Season = str(Contact.query.get(8 + offset*contactOffset).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def ButcherEff(currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(hover.jobMap['butcher'] + offset*contactOffset)
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
    Season = str(Contact.query.get(8 + offset*contactOffset).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def BuilderEff(currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(hover.jobMap['builder'] + offset*contactOffset)
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
    Season = str(Contact.query.get(8 + offset*contactOffset).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

