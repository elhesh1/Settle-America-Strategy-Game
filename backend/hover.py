from models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork
import buildings

def hoverString(type):
    if type == 'health':
        return healthString()
    return jobString(type)

jobMap = {'farmer': 1, 'hunter': 2, 'cook': 3, 'logger' : 4, 'butcher' : 11, 'builder' : 15}

def jobString(type):
    print("TYPE : ", type)
    JobValue = Contact.query.get(jobMap[type])
    Season = str(Contact.query.get(8).value)
    baseEfficiency = JobValue.efficiency['e']
    seasonEfficiency = JobValue.efficiency['season'][Season]
    string = ''
    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Efficiency Factors</div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Base'
    string += '</div> <div style="text-align: right;">'
    string += str(baseEfficiency)
    string +=  '</div></div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Season'
    string += '</div> <div style="text-align: right;">'
    string += str(seasonEfficiency)
    string +=  '</div></div>'

    if type == 'farmer':
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Iron Axe  (10) '
        string += '</div> <div style="text-align: right;">'
        string += 'X'
        string +=  '</div></div>'

        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (0)'
        string += '</div> <div style="text-align: right;">'
        string += 'X'
        string +=  '</div></div>'

        totalEfficiency = baseEfficiency * seasonEfficiency

        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Total '
        string += '</div> <div style="text-align: right;">'
        string += str(round(totalEfficiency,3))
        string +=  '</div></div>'
        
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

        count = JobValue.value
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Count: '
        string += '</div> <div style="text-align: right;">'
        string += str(count)
        string +=  '</div></div>'

        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(count * totalEfficiency) + ' Planted'
        string +=  '</div></div>'
    

        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'There are many factors that effect farming efficiency. Farmers dont need tools to work, but it greatly increases their efficiency </div>';
        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Most factors </div>'
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