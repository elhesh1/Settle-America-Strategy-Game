
from config import app, db
from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
from flask import request, jsonify
from variableHelpers import initial_variables
import advance
import hover
nFoodTypes = 0 

def eat():
    global foodTypes
    rationingPval = Contact.query.get(12).value
    expectedFood = rationingPval * 0.01 * Contact.query.get(5).value * 0.02 
    eatHelper(expectedFood)
    if  Contact.query.get(5).value != 0:
        housedRatio  = Building.query.get(1).value * Building.query.get(1).capacity / Contact.query.get(5).value # may want to change this one as well
    else:
        housedRatio = 0
    season = Contact.query.get(8)
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
    HealthCurrent = Contact.query.get(13)
    NumberFoodTypes = Contact.query.get(17)
    NumberFoodTypes.value = nFoodTypes

    HealthCurrent.value = round(HealthEquilibrium,0)

    db.session.commit()

    return jsonify({"message": " Values updated"}), 201

def eatHelper(expectedFood):
    global nFoodTypes
    FoodTypeValues = [0,0,0,0]
    nFoodTypes = 0
    # fruits, vegtables, meat, grain        
    FoodTypeValues[0] = Resource.query.get(8).value
    FoodTypeValues[1] = Resource.query.get(9).value
    FoodTypeValues[2] = Resource.query.get(7).value
    FoodTypeValues[3] = Resource.query.get(6).value
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
        val8  = Resource.query.get(8)
        val7 = Resource.query.get(7)
        val6 = Resource.query.get(6)
        val9 = Resource.query.get(9)
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
        val8  = Resource.query.get(8)
        val7 = Resource.query.get(7)
        val6 = Resource.query.get(6)
        val9 = Resource.query.get(9)
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
        eatHelper(foodleft)

    db.session.commit()

def build(): #16
    global weeklyBuildPower
    weeklyBuildPower = BuilderEff()[2] 
    index = Contact.query.get(16).value - 1
    current = CurrentlyBuilding.query.all()
    for i in range(index, len(current)):        # iterate through each building
        c = current[i]
        buildbuild(c,i)
    rows = CurrentlyBuilding.query.all()
    for row in rows:
        if row.value == 0:
            db.session.delete(row) 
    db.session.commit()


def buildbuild(c,i):
    global weeklyBuildPower
#    print(CurrentlyBuildingNeedWork.query.first() , "   INCLUDES")
    if CurrentlyBuildingNeedWork.query.first() is None:
        if c.value > 0:             
            building = Building.query.get(c.name)
            good = 0
            for key in building.cost:                       # iterate through each building requeremint
                resource = Resource.query.get(key)  # '5'
                costA = building.cost[key]
                if  costA > resource.value:
                    good = 1
                else:
                    resource.value -= costA
                    db.session.add(resource)
            if good == 0:
                c.value -= 1
                c.value = round(c.value,0) ### this should be added to ACTIVE. then use up builders. Maybe have an active queue as
                print("HAVE RESOURCES TO BUILD")
                db.session.commit()
                if building.work <= weeklyBuildPower: # we have enough power to build it this week 
                    print("ENOUGH POWER TO BUILD ", building.work, " ", weeklyBuildPower)
                    weeklyBuildPower -= building.work
                    building.value += 1
                    db.session.commit()
                    buildbuild(c,i)
                else:
                    c.value += 1
                    c.value = round(c.value,0)
                    print( "NOW ENOUGH POWER :(", building.work, " ", weeklyBuildPower)
                    currentBuilding = CurrentlyBuildingNeedWork(name = building.id , value = building.work-weeklyBuildPower)
                    db.session.add(currentBuilding)
                    db.session.commit()
                    print(currentBuilding.value)
        else:
            db.session.rollback()
    else:
        CurrentlyBuildingNeedsMoreWork = CurrentlyBuildingNeedWork.query.get(1)
        print("YOU ALREADY GOT SOME SHIT IN THERE")
        print(CurrentlyBuildingNeedsMoreWork.value, "   ", weeklyBuildPower)
        if CurrentlyBuildingNeedsMoreWork.value > weeklyBuildPower:
            CurrentlyBuildingNeedsMoreWork.value -= weeklyBuildPower
            weeklyBuildPower = 0 
            db.session.add(CurrentlyBuildingNeedsMoreWork)
            db.session.commit()
        else:
            weeklyBuildPower -= CurrentlyBuildingNeedsMoreWork.value
            buildingType = Building.query.get(CurrentlyBuildingNeedsMoreWork.id)
            buildingType.value += 1
            c.value -= 1
            c.value = round(c.value,0)
            db.session.query(CurrentlyBuildingNeedWork).delete()
            db.session.add(buildingType)
            db.session.commit()
            buildbuild(c,i)

def farmerEff(season):
        JobValue = Contact.query.get(hover.jobMap['farmer'])
        baseEfficiency = JobValue.efficiency['e']
        strength = Contact.query.get(18).value * 0.01
        Season = str(Contact.query.get(8).value)
        seasonEfficiency = JobValue.efficiency['season'][Season]
        count = int(JobValue.value)
        if int(season) == 1:
            print("SPRING")
            IronHoeMax = int(Resource.query.get(10).value)
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
            return IronHoeEfficiency, UsingIronHoe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, count * totalEfficiency, 'Iron Hoe', 'Planted'
        else: 
            print("NOT SPRING")
            IronSickleMax = int(Resource.query.get(11).value)
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
            return IronSickleEfficiency, UsingIronSickle, UsingNoTools, NoToolEfficiency, totalEfficiency, count, count * totalEfficiency, 'Iron Sickle', 'Harvested'

def LoggerEff():
    JobValue = Contact.query.get(hover.jobMap['logger'])
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18).value * 0.01
    Season = str(Contact.query.get(8).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    IronAxeMax = int(Resource.query.get(12).value)
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

def HunterEff():
    JobValue = Contact.query.get(hover.jobMap['hunter'])
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18).value * 0.01
    Season = str(Contact.query.get(8).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    RifleMax = int(Resource.query.get(13).value)
    BowMax = int(Resource.query.get(14).value)
    RifleEfficiency = 1.4
    BowEfficiency = 0.8
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

def CooksEff():
    JobValue = Contact.query.get(hover.jobMap['cook'])
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18).value * 0.01
    Season = str(Contact.query.get(8).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def ButcherEff():
    JobValue = Contact.query.get(hover.jobMap['butcher'])
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18).value * 0.01
    Season = str(Contact.query.get(8).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def BuilderEff():
    JobValue = Contact.query.get(hover.jobMap['builder'])
    baseEfficiency = JobValue.efficiency['e']
    strength = Contact.query.get(18).value * 0.01
    Season = str(Contact.query.get(8).value)
    seasonEfficiency = JobValue.efficiency['season'][Season]
    count = int(JobValue.value)
    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 