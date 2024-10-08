function makeTable(tabI) { // makes function table
    var result = "<table style='border-collapse: collapse;   font-size: 2vh;  >"; 
    for (var i = 0; i < tabI.length; i++) {
        if (tabI[i] != undefined) {
            result += "<tr style='height: 3vh;'>"; 
            for (var j = 0; j < tabI[i].length; j++) {
                result += "<td style='width: 50vh;'>" + tabI[i][j] + "</td>"; 
            }
            result += "</tr>"; 
        }         

    }
    result += "</table>"; 
    return result; 
}

async function getResources() {
    try {
        const response = await fetch(backendpath + `/resources/${currUserName}`);
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
            let temper = 0
            if (!((bruh[i]['value'] == 0) && (bruh[i]['always'] == 1))) {
                inventoryValues[i] = []; 
                inventoryValues[i][0] = bruh[i]['name'];
                    if (bruh[i]['integer'] == 0) {
                        inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(0);
                    }
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
        const response = await fetch(backendpath + `/buildings/${currUserName}`);
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
        let response = await fetch(backendpath + `/currentContent/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let string = "<table><thead><tr><th>Name</th><th>Value</th><th>  </th><th></th></tr></thead><tbody>";
        const BQueue = await response.json();
        let b2 = BQueue['buildingList'] // b2 is just the list of buildings
        let buildings = BQueue['buildings']
        
        for (let i = 0 ; i < buildings.length ; i++) {
            let building = buildings[i]
            console.log("THIS IS important it is the buildings", buildings)
            console.log(buildingNames)
            if (building['type'] === undefined) {
                btype = buildingNames[building['name']]
                if (building['name'] == 2){
                    btype = 'Town Hall'
                } else if (building['name'] == 7) {
                    btype = 'Tool Shop'
                }
                string += `<tr><td>${btype}</td><td>${building['value']}</td><td>${' ' }</td></tr>`;

            } else {
                console.log("BUIDLINGS", b2)
                console.log(buildings)
                console.log(i)
                buildingOffset = (Object.keys(b2).length)
                console.log("BUILDING OFFSET ", Object.keys(b2).length)
                numberName = buildings[i]['name']
                console.log(numberName, "   ", buildingOffset)
                while( numberName > buildingOffset) {
                    numberName -= buildingOffset
                    console.log("NEW NUMBER NAME ", numberName)
                }
                numberName -= 1
                console.log("NUMBER NAME  ; ", numberName)
                totalWork = b2[numberName]['work'];
                
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
        console.log("STRING : ", string)
        for (id in b2) {
            let elementtoUpdate = b2[id].name + 'currently';
            // console.log("b2  ", b2)
            // console.log("elementtoTupdate, ", elementtoUpdate)
            document.getElementById(elementtoUpdate).textContent = b2[parseInt(id)]['value']
        }
    } catch (error) {
        console.error('There was a problem coudlnt get the current buildings :', error);
        throw error;
    }
}
