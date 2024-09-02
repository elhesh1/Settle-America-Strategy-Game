const e = require("express");

window.onload = function() {
   setGame();
}


backendpath = `https://americagame-d4e96c50eefc.herokuapp.com/`
async function setGame() { // this sets up all the functions
    reset.addEventListener('click', resett);
    await resett()
    await  activateBackEndFunction('backEndSetUp');

    cookies = getCookie()
    console.log("COOKIES  ", cookies)
    if (cookies.includes("userID")) {
        console.log("Already set this one up")
    }
    else {
        console.log("set up a new cookie")
        setCookie('userID', generateUUID(), 365)
    }



    hoverMap =       {
        'FarmerJobGrid'  : ['FarmerJobToolTip','FarmersToolTipText','Job','farmer',1],
        'HuntersJobGrid' : ['HuntersJobToolTip','HuntersToolTipText','Job','hunter',2],
        'CooksJobGrid' : ['CooksJobToolTip','CooksToolTipText','Job','cook',3],
        'LoggersJobGrid' : ['LoggersJobToolTip','LoggersToolTipText','Job','logger',4],
        'ButchersJobGrid' : ['ButchersJobToolTip','ButchersToolTipText','Job','butcher',11],
        'BuilderJobGrid' : ["BuildersJobToolTip",'BuildersToolTipText','Job','builder',15],
        'topFoodBar' : ['HealthToolTip','HealthToolTipText' , 'Value'],
        'RationGrid' : ['RationToolTip', 'RationToolTipText', 'Value'],
        'Strength' : ['StrengthToolTip','StrengthToolTipText', 'Value'],
        'TownHallBuildGrid' : ['TownHallToolTip','TownHallToolTipText', 'Value', '.TownHall'], 
        'peopleSupply' : ['peopleSupplyToolTip','peopleSupplyToolTipText', 'Supply','peopleSupply'],
        'toolSupply' : ['toolSupplyToolTip','toolSupplyToolTipText', 'Supply','toolSupply'],
        'resourceSupply' : ['resourceSupplyToolTip','resourceSupplyToolTipText', 'Supply','resourceSupply'],
        'EnglandExplanation' : ['englandExplanationToolTip', 'englandExplanationToolTipText', 'other', 'EnglandExplanation'],
        'HealthGrid2' :  ['HealthToolTip','HealthToolTipText' , 'Value'],
        'PlantedGrid' : ['PlantedToolTip', 'PlantedToolTipText', 'Value', 'PlantedGrid'],
        'ToolShopBuildGrid' : ['ToolShopToolTip', 'ToolShopToolTipText','Value', '.ToolShop']
    }
    await buildingSetUp() /// and country set up
    var slider = document.getElementById("myRange");
    var sliderValueElement = document.getElementById("sliderValue");
    sliderValueElement.textContent = slider.value;
    slider.addEventListener("input", function() {
      sliderValueElement.textContent = slider.value;
    });


    const buttons = document.querySelectorAll('.B');           
        buttons.forEach(button => {
        button.addEventListener('click', buttonAction);
    });
    reset.addEventListener('click', resett);
    const nextW = document.getElementById('NextW');                 
    nextW.addEventListener('click', async function() {
        nextW.disabled = true; 
        try {
            await advance(); 
        } catch (error) {
            console.error('Error:', error);
        } finally {
            nextW.disabled = false; 
        }
    });
    const AdjustB = document.querySelectorAll('.Adjust');
        AdjustB.forEach(AdjB => {
            AdjB.addEventListener('click',changeValueOfInputForJobs);
        });

    document.getElementById('Clear').addEventListener('click', clearJobs);

    const buttonsB = document.querySelectorAll('.BuildingButton');                
        buttonsB.forEach(buttonB => {
        buttonB.addEventListener('click', buttonActionBuilding);
        });
    const buttonsBW = document.querySelectorAll('.BuildingButtonWorkers');                
        buttonsBW.forEach(buttonBW => {
        buttonBW.addEventListener('click', buttonActionBuildingWorkers);
        });
    reset.addEventListener('click', resett);
    const buttonsBU= document.querySelectorAll('.BuildUpgrade');                
        buttonsBU.forEach(buttonBU => {
        buttonBU.addEventListener('click', buttonActionBuildingUpgrade);
        });
    reset.addEventListener('click', resett);


    const buttons3 = document.querySelectorAll('.jobGrid');            
        buttons3.forEach(button3 => {
        button3.addEventListener('mouseover', toggleHover,false);
        button3.addEventListener('mouseleave', toggleHoverOff,false);
        });
    const buttons4 = document.querySelectorAll('.BuildingGrid');                
        buttons4.forEach(button4 => {
        button4.addEventListener('mouseover', toggleHover,false);
        button4.addEventListener('mouseleave', toggleHoverOff,false);
        });  
        
    getQueue();
    reset.addEventListener('click', resett);
    document.getElementById('CountriesT').click();      //              ///////// Opening Tab ///////////////
    await showValues();

    const buttons5 = document.querySelectorAll('.Hover');                
    buttons5.forEach(button5 => {
    button5.addEventListener('mouseover', toggleHover,false);
    button5.addEventListener('mouseleave', toggleHoverOff,false);
    });  
    const buttons6 = document.querySelectorAll('.HoverSupply');
    buttons6.forEach(button6 => {
    button6.addEventListener('mouseover', toggleHover,false);
    button6.addEventListener('mouseleave', toggleHoverOff,false);
    }); 

    }

async function activateBackEndFunction(input) {
    const response = await fetch(backendpath + `/${input}/${currUserName}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    });
    const responseData = await response.json();
}

async function buildingSetUp() {
     
    let buildings = await fetchBuildingCostMap();
    buildings = buildings['buildings']
    console.log( "BUILDINGS :: ", buildings)
    await countrySetUp()
    for (let i = 0; i < buildings.length; i++) {
        currentBuilding = buildings[i]
        let id = currentBuilding.id
        let fullName = currentBuilding.fullname
        let nameB = currentBuilding.name
        if (currentBuilding.work > 0 ) {
            let type = currentBuilding.typeOfBuilding
            hoverMap[nameB + 'BuildGrid'] = [nameB + 'ToolTip', nameB + 'Inner', type, nameB, id];
            let string = '<div class="BuildingGrid" id = "'  + nameB + 'BuildGrid"><h5 class="BuildingTitle" id="' + nameB + '">' + fullName + '</h5><button class="BuildingButtonUp BuildingButton '+ nameB + '" >+'
            string += '</button> <button class="BuildingButtonDown BuildingButton '+ nameB + '" >-</button><h5 class="BuildingNumberCurrent"  id="'+ nameB + 'Current">0</h5>'
            if(currentBuilding.typeOfBuilding != "Housing") {
                string += '<h5 class="BuildingpeopleWorking"  id="' + nameB + 'peopleWorking' +  '">' +  currentBuilding.working['value'] + '</h5>'
                string += '<h5 class="slash"  id="' + nameB + 'peopleWorking' +  '">' + '/'+ '</h5>'
                string += '<h5 class="BuildingpeopleCap"  id="' + nameB + 'peopleCap' +  '">' +  currentBuilding.working['maximum'] + '</h5>'
                string += '<button class="BuildingButtonWorkersUp BuildingButtonWorkers '+ nameB + '" >+</button>'
                string += '<button class="BuildingButtonWorkersDown BuildingButtonWorkers '+ nameB + '" >-</button>'

            }
            string += '<h5 class="BuildingNumberAlreadyBuilt"  id="' + nameB + 'currently' +  '">0</h5></div>'
            const nextW = document.getElementById('building-flex-container');
            nextW.innerHTML += string; 
            let hoverString = '<span class="jobToolTip" id="'+ nameB + 'ToolTip">'   
            hoverString += '<h5 class="ToolTipTitle">'+ fullName + '</h5>'
            hoverString += '<h3 class="ToolTipText" id="' + nameB + 'ToolTipText">' + type + '</h3>'
            hoverString += '<div class="flex-container" id="'+ nameB + 'Inner"></div></span>'
            const grid = document.getElementsByClassName('grid-container')[0];
           grid.innerHTML += hoverString
        }
        buildingNames[id] = fullName
        namesBuilding[nameB] = [id,0]
     }
     return


}


async function showValues() {
    let contacts = await getContacts()
    contacts = contacts.contacts
    document.getElementById('A').innerText = contacts['5']['value']
    document.getElementById('F').innerText = contacts['0']['value']
    document.getElementById('H').innerText = contacts['1']['value']
    document.getElementById('C').innerText = contacts['2']['value']
    document.getElementById('L').innerText = contacts['3']['value']
    document.getElementById('B').innerText = contacts['10']['value']
    document.getElementById('W2').innerText = contacts['14']['value']
    document.getElementById('HealthTopN').innerText = contacts['12']['value']
    document.getElementById('HealthNTab').innerText = contacts['12']['value']
    document.getElementById('W').innerText = contacts['6']['value']

    season = 'Winter'
    switch (contacts['7']['value']) {
        case 1:
            season = 'Spring'
            break;
        case 2:
            season = 'Summer'
            break;
        case 3:
            season = 'Fall'
            break;
    }
    document.getElementById('Season').innerText = season
}
async function buttonAction() { 
    let id = this.id
    let jobID = buttonMap[id][0]
    let type = labelMap[jobID][0]
    updatee('contact/', jobID, {value: buttonMap[id][1]}) // updates in db
    .then(() => {                           // retrieves val from db
        getValue('contacts/',jobID)
            .then(value => {
                document.getElementById(type).innerText = value;    
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById(type).innerText = 'Error fetching data';
            });
        getValue('contacts/',6)
            .then(value => {
                document.getElementById('A').innerText = value;
                tooltipSetupBuilding(hoverMap[labelMap[jobID][2]])
            })
            .catch(error => {
                console.error('Error fetching data for jobID 6:', error);
                document.getElementById('A').innerText = 'Error fetching data';
            });
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });
}

let BuildingChange = {};

function buttonActionBuilding() {
    let buildingType = this.className.split(' ')[2];
    let buildingNum = namesBuilding[buildingType][0];
    let changeName = buildingType += 'Current'
    changeNumber = 1
    if (this.className.includes('BuildingButtonDown')) {
        changeNumber = -1;
    }

    if (!Array.isArray(BuildingChange[buildingNum])) {
        BuildingChange[buildingNum] = [0]; 
    }
    BuildingChange[buildingNum][0] += changeNumber;
    if (BuildingChange[buildingNum][0] < 0) {
        BuildingChange[buildingNum][0] = 0;
    }
    const newval = BuildingChange[buildingNum][0];
    const element = document.getElementById(changeName);

    if (element) {
        element.innerText = newval;
    } else {
        console.error("Element with id:", changeName, "not found.");
    }

}

async function buttonActionBuildingUpgrade() {        // get the value of the building from Building and input that level in BuildingChange...., but make sure its the level and not the value
    const id = this.id
    changeName =   BuildingIDs[id][0]
    buildingNum = BuildingIDs[id][1]
    changeNumber = BuildingIDs[id][2]
 

    if (!Array.isArray(BuildingChange[buildingNum])) {
        BuildingChange[buildingNum] = [0,0]; 
    }
    let buildingCurrently = await getBuilding(buildingNum)
    if (BuildingChange[buildingNum][0] == 0){
        BuildingChange[buildingNum][1] = buildingCurrently['buildingInfo']['value'] + 1;
        BuildingChange[buildingNum][0] = 1;
        thisdude = document.getElementById(id);
        thisdude.className += " active";
    }
    else {BuildingChange[buildingNum][1] = buildingCurrently['buildingInfo']['value']
        BuildingChange[buildingNum][0] = 0;
        thisdude = document.getElementById(id);
        thisdude.className = thisdude.className.replace(" active", "").trim();
    }
}

async function resett() {     // function from resett it is used 
    console.log("STARTING RESET")
    document.getElementById("Season").textContent = "Spring";
    document.getElementById('One').click();
    const requestSupply = document.querySelectorAll('.requestSupply');
    requestSupply.forEach(rs => {
        rs.className = rs.className.replace(" active", "");
    });
    resettHelper()
    .then(() => {
        Object.keys(labelMap).forEach(key => {
            getValue('contacts/',key) 
            .then(value => {
                document.getElementById(labelMap[key][0]).innerText = value;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById(labelMap[key][0]).innerText = 'Error fetching data';
            });
        });
    })
    .then(() => {
        tableMaker()  
    })
    .then(() => {
        getQueue()
        buildingsShowing()
        tabSetUp()
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });

}

async function resettHelper() {
    currUserName = "placeholder999"
    await tabReset();
    try {
         const response = await fetch(backendpath + `/reset/${currUserName}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({userName : currUserName}),
            });
            const responseData = await response.json();
        }
        catch (error) {       // did not work
            console.error('Error BROKE BROKE:', error);
        }
}



async function getValue(type,user_id) {

    try {
        const response = await fetch(backendpath + `/${type}${user_id}/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.value;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

async function updatee(type, user_id, options) {
    
    const data = {};

    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    // set up data yk

     try {      // try to patch that john
        const response = await fetch(backendpath + `/update_${type}${user_id}/${currUserName}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });


        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();

    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}

var activeTab = "";

async function openTab(id, value) {
    tabcontent = document.getElementsByClassName("tabcontent"); // hid all other Tabs doggg
    for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
    }
    document.getElementById(value).style.display = "grid"

    activeTab = id;
    tabB = document.getElementsByClassName("tabB");
    for (i = 0; i < tabB.length; i++) {
        tabB[i].className = tabB[i].className.replace(" active", "");
    }
    if (id == 'FoodT') {
        foodTabSetUp();
    }
    else if (id == 'BuildingsT') {
        buildingTabSetUp(-1, -1);
    }
    else if (activeTab == 'InventoryT'){
        inventoryTabSetUp();
    }
    else if (activeTab == 'CountriesT') {
        countrySetUp()
        
    }
    else if(activeTab == 'FactoryT') {
        factorySetUp()
    }
    thisdude = document.getElementById(id);
    thisdude.className += " active";
}

async function setVal(type, user_id, options) {
    const data = {};
    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    try {     
        const response = await fetch(backendpath + `/set_${type}${user_id}/${currUserName}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });
        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const responseData = await response.json();
    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}

async function foodParagraphHelper() {
    let pop = await getValue('contacts/',5)
    let fp = document.getElementById('FoodParagraph')
    let totNeeded = Math.round(pop * 0.2) / 10
    let string =  "Every citizen needs 0.02 food a week to be fully fed. With a population of " + pop + ", " + totNeeded + " food is needed every week to keep them at full strength";
    fp.innerText = string;
}

function foodParagraph() {
   foodParagraphHelper()
   .then(iv => {
        foodpopcontainer.innerHTML = iv; 
    })
    .catch(error => {
    console.error("Error in tester:", error);
    });
}

function changeValueOfInputForJobs() {
    id = this.id
    setVal('contact/',14, {value: jobMulti[id] } )

    const AdjustB = document.querySelectorAll('.Adjust');
        AdjustB.forEach(AdjB => {
            AdjB.className = AdjB.className.replace(" active", "");
    });

    thisdude = document.getElementById(id);
    thisdude.className += " active";

    return 
}

async function clearJobs() {
    const response = await fetch(backendpath + `/clearJobs/${currUserName}`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),  
    })
        for (let key in labelMap) {
            if( labelMap[key][1] == "JOB") {
                jobb = document.getElementById(labelMap[key][0]);
                jobb.innerText = 0;
            }
        }
    let av = await getValue('contacts/',6)
    aval = document.getElementById('A');
    aval.innerText = av
}

async function getContact(id) {
    const response = await fetch(backendpath + `/contact/${id}/${currUserName}`, {
        method: 'GET', 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json();
    return data;
}

async function getContacts() {
    console.log ("currUserName : ", currUserName)
    const response = await fetch(backendpath + `/contacts/${currUserName}`, {
        method: 'GET', 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json();
    console.log("contacts", data)
    return data;
}

async function buttonActionBuildingWorkers() {
    let classList = this.className.split(' ')
    let workerChange = 1
    let buildingName = classList[2]
    let buildingID = namesBuilding[buildingName][0]
    if (classList[0] == 'BuildingButtonWorkersDown') {
        workerChange = -1
    }
    await updatee('building/', buildingID, {value: workerChange})
    let building = await getBuilding(buildingID) 
    currentlyWorking =  building['buildingInfo']['name']   + "peopleWorking"
    document.getElementById(currentlyWorking).innerText = building['buildingInfo']['working']['value']
    let value = await getValue('contacts/',6)
    document.getElementById('A').innerText = value;
    // + "BuildGrid"
    await tooltipSetupBuilding(hoverMap[buildingName+ "BuildGrid" ])
}

async function countrySetUp() {
    try {
        const response = await fetch(backendpath + `/countryInnerString/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        nativeString =      await countrySetUpNative()
        inner = document.getElementById('countries-flex-container')
        inner.innerHTML =  data['string']  + nativeString
        let buttons3 = document.querySelectorAll('.requestSupply');            
        buttons3.forEach(button3 => {
        button3.addEventListener('mouseover', toggleHover,false);
        button3.addEventListener('mouseleave', toggleHoverOff,false);
        button3.addEventListener('click', setSupplyType)
        });

        let buttons2 = document.querySelectorAll('.TradeButton');
        buttons2.forEach(button2 => {
            button2.addEventListener('click', tradeButton);
        });
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}


async function tradeButton() {
    id = this.id
    id = id.replace("TradeButton","")
    try {
 
        const response = await fetch(backendpath + `/trade/${currUserName}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'buttonName' : id}),  
        });
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

async function countrySetUpNative() {
    flexInner = document.getElementById('countries-flex-container');
    try {
        const response = await fetch(backendpath + `/countryInnerStringNative/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        return data['string'];
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

// Call the function when the DOM is loaded
document.addEventListener('DOMContentLoaded', (event) => {
    currUserName = "placeholder999"

    countrySetUpNative();
});
activeSupplyType = undefined
function setSupplyType() {
    const requestSupply = document.querySelectorAll('.requestSupply');
    requestSupply.forEach(rs => {
        rs.className = rs.className.replace(" active", "");
    });
    activeSupplyType = this.id
    this.classList += " active"
}

function getCookie() {
    let decodedCookie = decodeURIComponent(document.cookie);
   // let ca = decodedCookie.split(';');
    return decodedCookie;
  }

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = `${cname}=${cvalue};${expires};path=/`;
  }


function generateUUID() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}