
from config import app, db
from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
from flask import request, jsonify
from variableHelpers import initial_variables
import advance
nFoodTypes = 0
# to do 7/22 make health drop if you can't eat, and half empty foods count as empty
def eat():
    global foodTypes
    rationingPval = Contact.query.get(12).value
   # print("R  ",rationingPval)
    expectedFood = rationingPval * 0.01 * Contact.query.get(5).value * 0.02
    eatHelper(expectedFood)
   # print("R  ",rationingPval)
    HealthEquilibrium = rationingPval*0.01 * (68+nFoodTypes*8)
    HealthCurrent = Contact.query.get(13)
    if nFoodTypes == 0:
        HealthEquilibrium = 0 # could change the health to have an equlibrium not a thing currently
    HealthCurrent.value = round(HealthEquilibrium,0)
   # print("20      ", HealthCurrent.value, "  ", HealthEquilibrium )

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
    # now subtract the lesser of food min and 
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
        #
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


    builders = Contact.query.get(15)
    weeklyBuildPower = builders.value
    print("WEEKLY BUILD POWER   ", weeklyBuildPower)

    index = Contact.query.get(16).value - 1
    print(index)
    current = CurrentlyBuilding.query.all()
    print("AAAAAAAAAAAAAAAAAAAAAAAAA    ",current)
    for i in range(index, len(current)):        # iterate through each building
        c = current[i]
        buildbuild(c,i)


def buildbuild(c,i):
    global weeklyBuildPower
    print(CurrentlyBuildingNeedWork.query.first() , "   INCLUDES")

    if CurrentlyBuildingNeedWork.query.first() is None:
        if c.value > 0:             
        #  print( "   i ", i , "  c ", c)
            building = Building.query.get(c.name)
        #   print("BUILDING : ", c.id, " ", c.name , " ", c.value, "  ")
        #   print(building.cost)
            good = 0
            for key in building.cost:                       # iterate through each building requeremint
                resource = Resource.query.get(key)  # '5'
            #    print("keys open doors ", key)
                costA = building.cost[key]
                if  costA > resource.value:
                #   print("NAHHHH")
                    good = 1
                else:
            #     print("Re val : ", resource.value, "    Cost: ", costA)
                    resource.value -= costA
                    db.session.add(resource)
            if good == 0:


                c.value -= 1
                c.value = round(c.value,0) ### this should be added to ACTIVE. then use up builders. Maybe have an active queue as
                print("HAVE RESOURCES TO BUILD")
                db.session.commit()


                if building.work < weeklyBuildPower: # we have enough power to build it this week 
                    print("ENOUGH POWER TO BUILD ", building.work, " ", weeklyBuildPower)
                    weeklyBuildPower -= building.work
                    building.value += 1
                    db.session.commit()
                    buildbuild(c,i)
                else:
                    print( "NOW ENOUGH POWER :(", building.work, " ", weeklyBuildPower)
                    currentBuilding = CurrentlyBuildingNeedWork(name = building.id , value = building.work)
                    db.session.add(currentBuilding)
                    db.session.commit()
 # print("W  E CAN BUILD")

        else:
          #  print("CAN NOT BUILD")     
            db.session.rollback()
                    # GO TO NEXY ITEM IN QUEUE
   #     print("I'm Finished ")
    else:
        CurrentlyBuildingNeedsMoreWork = CurrentlyBuildingNeedWork.query.get(1)
        print("YOU ALREADY GOT SOME SHIT IN THERE")
        print(CurrentlyBuildingNeedsMoreWork.value, "   ", weeklyBuildPower)
        if CurrentlyBuildingNeedsMoreWork.value > weeklyBuildPower:
            print("CANT FINISH")
            CurrentlyBuildingNeedsMoreWork.value -= weeklyBuildPower
            weeklyBuildPower = 0 
            db.session.add(CurrentlyBuildingNeedsMoreWork)
            db.session.commit()
        else:
            print("can finish")
            weeklyBuildPower -= CurrentlyBuildingNeedsMoreWork.value
            buildingType = Building.query.get(CurrentlyBuildingNeedsMoreWork.id)
            buildingType.value += 1
            db.session.query(CurrentlyBuildingNeedWork).delete()
            db.session.add(buildingType)
            db.session.commit()
            buildbuild(c,i)
            ### HAS BEEN BUILT 

