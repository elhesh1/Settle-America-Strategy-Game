
window.onload = function() {
   setGame();
}

async function setGame() { // this sets up all the functions
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
    const buttons5 = document.querySelectorAll('.Hover');                
        buttons5.forEach(button5 => {
        button5.addEventListener('mouseover', toggleHover,false);
        button5.addEventListener('mouseleave', toggleHoverOff,false);
        });  
    getQueue();
    reset.addEventListener('click', resett);
    document.getElementById('InventoryT').click();      //              ///////// Opening Tab ///////////////
    await showValues();
    
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
function buttonAction() { 
    id = this.id
    var jobID = buttonMap[id][0]
    var type = labelMap[jobID][0]
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

BuildingChange = {}

function buttonActionBuilding() {
    id = this.id
    changeName =   BuildingIDs[id][0]
    buildingNum = BuildingIDs[id][1]
    changeNumber = BuildingIDs[id][2]
    if (BuildingChange[buildingNum]) {
        BuildingChange[buildingNum] += changeNumber;
        if (BuildingChange[buildingNum] < 0) {
            BuildingChange[buildingNum] = 0;
        }
    } else {
        BuildingChange[buildingNum] = changeNumber;
        if (BuildingChange[buildingNum] < 0) {
            BuildingChange[buildingNum] = 0;
        }
    }
    newval = BuildingChange[buildingNum];
    document.getElementById(changeName).innerText = newval
}


function resett() {     // function from resett it is used 
    document.getElementById("Season").textContent = "Spring";
    document.getElementById('One').click();
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
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });
}

async function resettHelper() {
    try {
         const response = await fetch('http://127.0.0.1:5000/reset', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });
            const responseData = await response.json();
        }
        catch (error) {       // did not work
            console.error('Error:', error);
        }
}

async function getValue(type,user_id) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/${type}${user_id}`);
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
        const response = await fetch(`http://127.0.0.1:5000/update_${type}${user_id}`, {
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

activeTab = "";

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
        const response = await fetch(`http://127.0.0.1:5000/set_${type}${user_id}`, {
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
    const response = await fetch(`http://127.0.0.1:5000/clearJobs`, {
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
    const response = await fetch(`http://127.0.0.1:5000/contact/${id}`, {
        method: 'GET', 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json();
    return data;
}

async function getContacts() {
    const response = await fetch(`http://127.0.0.1:5000/contacts/`, {
        method: 'GET', 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json();
    return data;
}
