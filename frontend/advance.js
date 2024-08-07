
async function advance() {   
    inputs = []
 

      for (const build in BuildingChange) {
        inputs.push({ 'name': build, 'value': BuildingChange[build] });
      }
      
    const response1 = await fetch(`http://127.0.0.1:5000/addCurr`, {

        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputs),  
    });
    if (!response1.ok) {
        throw new Error(`HTTP error! Status: ${response1.status}`);
    }
    const data1 = await response1.json();
    document.getElementById('xCL').textContent = 0;
    BuildingChange = {}


    await advanceJob();              // do jobs

    const response = await fetch(`http://127.0.0.1:5000/advancePackage`); // 5, 7, 13
    const data = await response.json();

    let w = data.contacts[7-1].value;  
    document.getElementById("W").textContent = w;
    if(w == 1) {
        let s = data.contacts[8-1].value
        switch(s) { 
            case 1:
                document.getElementById("Season").textContent = "Spring"; break;
            case 2:
                document.getElementById("Season").textContent = "Summer";  break; 
            case 3:
                document.getElementById("Season").textContent = "Fall"; break;
            case 0:
                document.getElementById("Season").textContent = "Winter"; 
                let y = data.contacts[9-1].value
                document.getElementById("Year").textContent = y; 
                break;

        }
    }
    document.getElementById("P").textContent = data.contacts[5-1].value
    document.getElementById("A").textContent = data.contacts[6-1].value

    var elements = document.getElementsByClassName("HealthN");
    if (elements.length > 0) {
        elements[0].innerText = data.contacts[13 - 1].value;
        elements[1].innerText = data.contacts[13 - 1].value;
    }

    if (activeTab == 'FoodT') {
        foodTabSetUp();
    }
    else if (activeTab == 'BuildingsT') {
             /// will have to update this perhaps
        buildingTabSetUp(data.contacts[5-1].value);
    }
    else if (activeTab == 'InventoryT'){
        inventoryTabSetUp();
    }



}

async function advanceJob() {
    await setVal('contact/', 12, {value : parseInt(document.getElementById("sliderValue").textContent)})

    const response = await fetch(`http://127.0.0.1:5000/advance`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify([]),  
    });
    let plantedcount = await getValue('contacts/',10);
    document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);//////////////////////////////////////////////////////////////////////
    getQueue();
 
}

