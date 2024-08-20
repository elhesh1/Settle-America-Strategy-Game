from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
import buildings
import citizenActions
import country
def hoverString(typee):
    if typee == 'health':
        return healthString()
    
    if str(typee)[0] == '.': 
        return buildingStringUpgrade(typee)
    if typee in jobMap:
        return jobString(typee)
    if typee == 'resourceSupply' or typee == 'peopleSupply' or typee == 'toolSupply':
        return country.supplyString(typee)
    if typee == 'EnglandExplanation':
        return country.supplyToolTip()
    return buildingToString(typee)

jobMap = {'farmer': 1, 'hunter': 2, 'cook': 3, 'logger' : 4, 'butcher' : 11, 'builder' : 15}

def jobString(typee):
    JobValue = Contact.query.get(jobMap[typee])
    season = str(Contact.query.get(8).value)
    baseEfficiency = JobValue.efficiency['e']
    seasonEfficiency = JobValue.efficiency['season'][season]
    strength = Contact.query.get(18).value * 0.01
    string = ''
    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Efficiency Factors</div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Base'
    string += '</div> <div style="text-align: right;">'
    string += str(baseEfficiency)
    string +=  '</div></div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Strength'
    string += '</div> <div style="text-align: right;">'
    string += str(round(strength,2))
    string +=  '</div></div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Season'
    string += '</div> <div style="text-align: right;">'
    string += str(seasonEfficiency)
    string +=  '</div></div>'

    if typee == 'farmer':
        if int(season) == 1 or int(season) == 3:
            farmingPower, IronHoeEfficiency, UsingIronHoe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, seasonTool, verb = citizenActions.farmerEff(season)
            string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
            string += seasonTool + ' ('  + str(UsingIronHoe) + ')'
            string += '</div> <div style="text-align: right;">'
            string += str(IronHoeEfficiency)
            string +=  '</div></div>'
        elif int(season) == 2:
            farmingPower, UsingNoTools, NoToolEfficiency, totalEfficiency, count, verb = citizenActions.farmerEff(season)
        else:
            a = citizenActions.farmerEff(season)
            farmingPower, UsingNoTools, NoToolEfficiency, totalEfficiency, count, verb = citizenActions.farmerEff(season)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)
        string +=  '</div></div>'

        string += efficiencyAndCount(totalEfficiency,count)
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(farmingPower,2)) + ' ' + verb
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'There are many factors that effect farming efficiency. Farmers dont need tools to work, but it greatly increases their efficiency </div>';
        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Most factors </div>'
            
    elif typee == 'logger':
        IronAxeEfficiency, UsingIronAxe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, loggingPower = citizenActions.LoggerEff()
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Iron Axe' + ' ('  + str(UsingIronAxe) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(IronAxeEfficiency)
        string +=  '</div></div>'

        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)
        string +=  '</div></div>'

        string += efficiencyAndCount(totalEfficiency,count)

        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(loggingPower,2)) + ' Wood'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'hunter':
        RifleEfficiency, UsingRifle, BowEfficiency, UsingBow, NoToolEfficiency, UsingNoTools, count, totalEfficiency, huntingpower = citizenActions.HunterEff()
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Rifle' + ' ('  + str(UsingRifle) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(RifleEfficiency)
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Bow' + ' ('  + str(UsingBow) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(BowEfficiency)
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)  
        string +=  '</div></div>'
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(huntingpower,2)) + ' Raw Meat'
        string +=  '</div>'
        string += '</div> <div class="flexitem" style="text-align: right;">'
        string += str(round(huntingpower,2)) + ' Fur</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'cook':
        totalEfficiency, count , cookingpower = citizenActions.CooksEff()
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Input: '
        string += '</div> <div style="text-align: right;">'
        string += '-' + str(round(cookingpower,2)) + ' Wheat'
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(cookingpower,2)) + ' Bread'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'butcher':
        totalEfficiency, count , butcherpower = citizenActions.ButcherEff()
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Input: '
        string += '</div> <div style="text-align: right;">'
        string += '-' +  str(round(butcherpower,2)) + ' Raw Meat'
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(butcherpower,2)) + ' Cooked Meat'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'builder':
        totalEfficiency, count , builderpower = citizenActions.BuilderEff()
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(builderpower,2)) + ' Work'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string

def healthString():
    nFoodTypes = Contact.query.get(17).value
    health = Contact.query.get(13).value 
    rationP = Contact.query.get(12).value
    pop = Contact.query.get(5).value
    housed = buildings.housingCapacity()
    string = ""
    string += '<div class="flexitem" style="text-align: left; width: 100%">'
    string += 'The health of your colony is very important as it effects citizens ability to do jobs. If your health falls below 50, citizens will start to die off'
    string += '</div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: left; width: 100%">' 
    string += 'Your current health of ' + str(health) + ' is affected by your rationing percentage of ' + str(rationP) + ' and number of food groups : ' + str(nFoodTypes) + '. Providing all 4 food groups is good for health, but only 1 is needed.'
    string += '</div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: left; width: 100%">'
    string += 'Lack of housing effects health. While it has a small effect in summer, it can be detrimental in the winter'
    string += '</div>'
    string +='<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Housing Provided: </div> <div style="text-align: right;">'+ str(housed) + '/' + str(pop) + '</div></div>'
    return string

def efficiencyAndCount(totalEfficiency,count):
        string = '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Total</div> <div style="text-align: right;">'
        string += str(round(totalEfficiency,3))
        string +=  '</div></div><div class="flexitem ToolTipLine" width="80%" size="4"></div><div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Count: </div> <div style="text-align: right;">'
        string += str(count) + '</div></div>'
        return string

buildingMap = {'TownHall' : 2}


buildingLevels = [
        {"capacity" : 0, "efficiency" : 1},
        { "capacity" : 10, "efficiency" : 1, "cost" : 5},
        { "capacity" : 30, "efficiency" : 1.02, "cost" : 10}


]

value = buildingLevels[1]['capacity']

def buildingStringUpgrade(typee):
    buildingString = typee.split(".")[1]
    print(" THISSSS?")
    building = Building.query.get(buildingMap[buildingString])
    builindgLevel = building.value
    string = ''

    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Current Level: ' + str(building.value)
    string += '</div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Capacity'
    string += '</div> <div style="text-align: right;">'
    string += str(buildingLevels[builindgLevel]['capacity'])
    string +=  '</div></div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Efficiency'
    string += '</div> <div style="text-align: right;">'
    string += str(buildingLevels[builindgLevel]['efficiency'])
    string +=  '</div></div>'


    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Upgrade Cost:'
    string += '</div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Work'
    string += '</div> <div style="text-align: right;">'
    string += str(buildingLevels[builindgLevel+1]['cost']) if builindgLevel+1 < len(buildingLevels) else 'Max'
    string +=  '</div></div>'

    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Upgrade Effects:'
    string += '</div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Capacity'
    string += '</div> <div style="text-align: right;">'
    string += '+' + str(round(buildingLevels[builindgLevel+1]['capacity'] - buildingLevels[builindgLevel]['capacity'],0)) if builindgLevel+1 < len(buildingLevels) else 'Max'
    string +=  '</div></div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Efficiency'
    string += '</div> <div style="text-align: right;">'
    string += '+' + str(round(buildingLevels[builindgLevel+1]['efficiency'] - buildingLevels[builindgLevel]['efficiency'],2)) if builindgLevel+1 < len(buildingLevels) else 'Max'
    string +=  '</div></div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string  

def buildingToString(typee):
    string = ''
    if typee in buildings.namesToIDs:
        currBuilding = Building.query.get(buildings.namesToIDs[typee])
        costList = currBuilding.cost
        if costList != None:
            string += '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + '</div>'
            for val in costList:
                string  +=' <div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">' + str(Resource.query.get(val).name)
                string += '</div> <div style="text-align: right;">' + str(costList[val]) + '</div></div>'
        string +=    '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Work</div> <div style="text-align: right;">' + str(currBuilding.work) +'</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
        if currBuilding.working is not None:
                toolEfficiency, UsingTool, UsingNoTools, NoToolEfficiency, totalEfficiency, count, baseEfficiency, otherFactors, toolName, strength  = buildings.buildingsEff(currBuilding) 
                string += '<div class="flexitem" style="text-align: center; width: 100%">'
                string += 'Efficiency Factors</div>'

                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                string += 'Base'
                string += '</div> <div style="text-align: right;">'
                string += str(baseEfficiency)
                string +=  '</div></div>'
                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                string += 'Strength: '
                string += '</div> <div style="text-align: right;">'
                string += str(strength)
                string +=  '</div></div>'
                if toolEfficiency != 0:
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += str(toolName) + '(' + str(UsingTool) +')'
                    string += '</div> <div style="text-align: right;">'
                    string += str(toolEfficiency)
                    string +=  '</div></div>'
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += 'No Tools' + '(' + str(UsingNoTools) +')'
                    string += '</div> <div style="text-align: right;">'
                    string += str(NoToolEfficiency)
                    string +=  '</div></div>'
                string += efficiencyAndCount(totalEfficiency,count)
                if  currBuilding.Inputs:
                    Inputs = currBuilding.Inputs
                    first = 0
                    for key in Inputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Input: '
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key] * totalEfficiency * count,2))+ ' '  + str(Resource.query.get(key).name)+ ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(key).name) + ' ' 
                            string +=  '</div></div>'
                if  currBuilding.Outputs:
                    Outputs = currBuilding.Outputs
                    first = 0
                    for key in Outputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Outputs: '
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(key).name) + ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(key).name) + ' ' 
                            string +=  '</div></div>'
                string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
            #  if currBuilding.Inputs == {}
                power = totalEfficiency* count

        string += description(typee)


    return string


def description(typee):
    currBuilding = Building.query.get(buildings.namesToIDs[typee])
    if typee == 'LogCabin':
        string = ''
        sum = round(currBuilding.value * currBuilding.capacity)
        string +=  '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">' + 'Each '+ 'log cabin' + ' can house ' +  str(currBuilding.capacity) +  ' people. The ' +  str(currBuilding.value) + " " + 'log cabin' + 's currently built house ' + str(sum) + ' citizens' +  '</div>'
        return string
    return ""
