function makeTable(tabI) { // makes function table
 //   console.log("tabI :  ", tabI)
    var result = "<table style='border-collapse: collapse;   font-size: 2vh;  >"; 
    for (var i = 0; i < tabI.length; i++) {
        result += "<tr style='height: 3vh;'>"; 
        for (var j = 0; j < tabI[i].length; j++) {
            result += "<td style='width: 50vh;'>" + tabI[i][j] + "</td>"; 
        }
        result += "</tr>"; 
    }
    result += "</table>"; 
    return result; 
}

async function getResources() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/resources`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        return data;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

async function takeInventory() {
    let inventoryValues = []; 
    try {
        let values = await getResources(); 
        let bruh = values.resources; 
        for (let i = 0; i < bruh.length; i++) {
            inventoryValues[i] = []; 
            inventoryValues[i][0] = bruh[i]['name'];
            if (bruh[i]['integer'] == 0) {
                inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(2);
            } else {
                inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(0);
            }
        }
            return inventoryValues; 
    } catch (error) {
        console.error("Error in takeInventory:", error);
        throw error; 
    }
}

function tableMaker() { 
    takeInventory()
    .then(iv => {
        let updatedTableHtml = makeTable(iv); 
        tableContainer.innerHTML = updatedTableHtml; 
    })
    .catch(error => {
        console.error("Error in tester:", error);
    });
}

async function fetchBuildingCostMap() {
    try {
        const response = await fetch('http://127.0.0.1:5000/buildings');
                if (!response.ok) {
            throw new Error('Network response was not ok');
        }
                const buildingCostMap = await response.json();        
        return buildingCostMap;
    } catch (error) {
        console.error('Error fetching building cost map:', error);
    }
}

async function getQueue() {
    try {
        let response = await fetch(`http://127.0.0.1:5000/currentContent`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let string = "<table><thead><tr><th>Name</th><th>Value</th><th>  </th><th>_______</th></tr></thead><tbody>";
        const BQueue = await response.json();
        let b2 = BQueue['buildingList'] // b2 is just the list of buildings
        let buildings = BQueue['buildings']
        for (let i = 0 ; i < buildings.length ; i++) {
            let building = buildings[i]
            if (building['type'] === undefined) {
                string += `<tr><td>${buildingNames[building['name']]}</td><td>${building['value']}</td><td>${building['type']}</td></tr>`;

            } else {
                totalWork = b2[buildings[i]['name']-1]['work'];
                if (totalWork == -1) {
                    //// get value from lookuptable
                    totalWork = 5
                }
                progress = totalWork-buildings[i]['value'] 
                string +=  '<tr><td colspan="3"><progress id="file" max="'+ totalWork + '" value="' +progress  +'"></progress></td></tr>';
            }
        }
        string += "</tbody></table>";
        buildingQueue.innerHTML = string
        for (id in b2) {
            let elementtoUpdate = b2[id].name + 'currently';
            document.getElementById(elementtoUpdate).textContent = b2[parseInt(id)]['value']
        }
    } catch (error) {
        console.error('There was a problem coudlnt get the current buildings :', error);
        throw error;
    }
}
