
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
            inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(2);
        }
            return inventoryValues; 
    } catch (error) {
        console.error("Error in takeInventory:", error);
        throw error; 
    }
}


function makeTable(tabI) {
    var result = "<table style='border-collapse: collapse; font-size: 2vh;  >"; 
    for (var i = 0; i < tabI.length; i++) {
        result += "<tr style='height: 20px;'>"; 
        for (var j = 0; j < tabI[i].length; j++) {
            result += "<td style='width: 14vh;'>" + tabI[i][j] + "</td>"; 
        }
        result += "</tr>"; 
    }
    result += "</table>"; 
    return result; 
}

function tableMaker() { 
    takeInventory()
    .then(iv => {
        var updatedTableHtml = makeTable(iv); 
                tableContainer.innerHTML = updatedTableHtml; 
    })
    .catch(error => {
        console.error("Error in tester:", error);
    });
}



async function getQueue() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/currentContent`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        /// potentially clean and sort the list so that the current buildings are where they should be
        string = "<table><thead><tr><th>Name</th><th>Value</th><th>  </th><th>_______</th></tr></thead><tbody>";


        const BQueue = await response.json();
        buildings = BQueue['buildings']
        console.log(typeof(buildings))
        for (let i = 0 ; i < buildings.length ; i++) {
            building = buildings[i]
            console.log("CURRENT BUILDING  ", buildings[i], "   " , buildings[i]['id'], " ", buildings[i]['name'], "  ",buildings[i]['value'], buildings[i]['type'] );
            if (building['type'] === undefined) {
                console.log( " not currently being built if ");
                string += `<tr><td>${buildingNames[building['name']]}</td><td>${building['value']}</td><td>${building['type']}</td></tr>`;

            } else {
                string += '<tr><td colspan="3">CurrentlyBuilding</td></tr>'
                console.log(" currently being built ");
            }
        }
        console.log(buildings.length)
        string += "</tbody></table>";

        
        var updatedTableHtml =  Math.random() ////
        buildingQueue.innerHTML = string





    } catch (error) {
        console.error('There was a problem coudlnt get the current buildings :', error);
        throw error;
    }
}
