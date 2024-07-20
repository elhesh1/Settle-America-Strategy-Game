// var tableTester = [
//     ["NAME", 1],
//     ["Name2", 2],
//     ["Name3", 3],
//     ["Name4", 4],
//     ["NAME", 1],
//     ["Name32", 22],
//     ["Name33", 31],
//     ["Name41", 14],    
//     ["Name21", 12],
//     ["Name31", 31],
//     ["Name41", 41]
// ];
// var inventoryValues = [];

// var tableTeste2r = [
//     ["NA22ME", 21],
//     ["Name2", 2],
//     ["Name3", 23],
//     ["Name4", 24],
//     ["NAME", 1],
//     ["Name32", 22],
//     ["Name33", 312],
//     ["Name41", 14],    
//     ["Name21", 1222],
//     ["Name31", 31],
//     ["Name41", 41]
// ];
async function getResources() {
    console.log("TAKING R")
    try {
        const response = await fetch(`http://127.0.0.1:5000/resources`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);

        return data;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}


async function takeInventory() {
    console.log(" GET RRR");

    let inventoryValues = []; 
    try {
        let values = await getResources(); 
        let bruh = values.resources; 
        for (let i = 0; i < bruh.length; i++) {
            inventoryValues[i] = []; 
            inventoryValues[i][0] = bruh[i]['name'];
            inventoryValues[i][1] = 300;
        }
            return inventoryValues; 
    } catch (error) {
        console.error("Error in takeInventory:", error);
        throw error; 
    }
}


function makeTable(tabI) {
    var result = "<table style='border-collapse: collapse;'>"; 
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