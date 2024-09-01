async function foodTabSetUp() {
    document.getElementById('StrengthB').innerText = await getValue('contact/',18)
    foodParagraphHelper();

}

async function buildingTabSetUp(pop, h) { 
    if (pop == -1) {  pop = await getValue('contacts/',5);}
    h = await getBuilding(1) 
    housed = h['buildingInfo'].value * h['buildingInfo'].capacity
    housingvalue = document.getElementById('HousingValue');
    string = 'Housing Provided: '+ housed + ' / ' + pop;
    housingvalue.innerText = string;
    
}

async function inventoryTabSetUp() {
    tableMaker();
}

async function tabReset() {

    if (activeTab == 'BuildingsT') {
        //BuildingpeopleWorkin
    }
    if (activeTab == 'CountriesT') {
        console.log("COUNTRIE T ACTIVATED")
    }

}

function tabSetUp() {
    if (activeTab == 'FoodT') {
        foodTabSetUp();
    }
    else if (activeTab == 'BuildingsT') {
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
}

async function buildingsShowing() {
    let buildings = await fetchBuildingCostMap();
    let currentlyWorkings = document.getElementsByClassName("BuildingpeopleWorking"); // actually keep this one out
    for (i = 0; i < currentlyWorkings.length; i++) {
        currentlyWorkings[i].innerText = buildings.buildings[namesBuilding[currentlyWorkings[i].id.replace('peopleWorking', '')][0]-1]['working']['value'];
    }
    let capWorkings = document.getElementsByClassName('BuildingpeopleCap');
    for (i = 0; i < currentlyWorkings.length; i++) {
        capWorkings[i].innerText =buildings.buildings[namesBuilding[currentlyWorkings[i].id.replace('peopleWorking', '')][0]-1]['working']['maximum'];
    }  
}

async function factorySetUp() {

    const response = await fetch(`http://127.0.0.1:5000/factoryTab/${currUserName}`);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    inner = document.getElementById('FactoryFlex')
    inner.innerHTML =  data['string']

    let buttons2 = document.querySelectorAll('.TradeButton');
    buttons2.forEach(button2 => {
        button2.addEventListener('click', tradeButton);
    });
}