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