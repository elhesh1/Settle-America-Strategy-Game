async function foodTabSetUp() {

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