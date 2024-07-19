var tableTester = [
    ["NAME", 1],
    ["Name2", 2],
    ["Name3", 3],
    ["Name4", 4],
    ["NAME", 1],
    ["Name32", 22],
    ["Name33", 31],
    ["Name41", 14],    
    ["Name21", 12],
    ["Name31", 31],
    ["Name41", 41]
];
var inventoryValues = [];

var updatedTableData = [
    ["Updated 1, 1", "Updated 1, 2", "Updated 1, 3"],
    ["Updated 2, 1", "Updated 2, 2", "Updated 2, 3"]
];



function takeInventory() {
    for (var i = 0; i < 2; i++) {
        inventoryValues[i] = []; 
        for (var j = 0; j < 2; j++) {
            inventoryValues[i][j] = i + j;
        }
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

function tester() {
    takeInventory();
    console.log(inventoryValues)
    console.log ("TESTING TESTING");
    var updatedTableHtml = makeTable(updatedTableData);
    console.log(updatedTableHtml)
    tableContainer.innerHTML =  makeTable(updatedTableHtml);
}