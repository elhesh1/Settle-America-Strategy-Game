
async function advance() {
    var weak = 0;
    await advanceJob();              // do jobs
    updatee('contact/',7,{value : 1})
    .then(() => {                           // retrieves val from db
        getValue('contacts/',7)
        .then(value => {
                weak = value;
            })
                                            // change weeks
            .then(() => {
                value = weak;
                if (value == 14) { //       NEW SEASON
                    value = 1;
                    updatee('contact/', 7,{value : -13});
                    getValue('contacts/',8)
                    .then(value => {  //gets season val
                        let season = (value + 1)%4 
                        switch(season) {
                            case 1:
                                document.getElementById("Season").textContent = "Spring"; break;
                            case 2:
                                document.getElementById("Season").textContent = "Summer";  break; 
                            case 3:
                                document.getElementById("Season").textContent = "Fall"; break;
                            case 0:
                                document.getElementById("Season").textContent = "Winter"; break;
                        }
                        setVal('contact/',8, {value :season }); 
                        

                    })
                } 
                document.getElementById("W").innerText = value; 
            

            })
    })
    return true;
}

async function advanceJob() {
    await advanceCooks();
    await advanceButchers();
    await advanceHunters();
    await advanceLoggers();
    await advancePlanters();
    tableMaker();
 
 
}




async function advanceLoggers() {
    let logging = await getValue('contacts/', 4)
    woodChange = logging * 0.1;
    await updatee('resources/', 5, { value: woodChange })
        
}
async function advanceButchers() {
    let toAdd = 0;
    let butchers = await getValue('contacts/',11); //gets# of butchers
    cookingPower = butchers * 0.1;
    await updatee('resources/', 4, {value: -1 * cookingPower}) // takes out raw meat
    left = await getValue('resources/',4);  // this is the value of the wheat that we have
    if (left < 0) {
        toAdd = left
    }       // toAdd back up bc you can't have negative resources
    await updatee('resources/',4, {value: -toAdd})  //wheat moves back to 0
    await updatee('resources/',7, {value : cookingPower + toAdd}) //change bread values;   




}
async function advancePlanters() {

        let plantingCount = await getValue('contacts/', 1);
        let season = await getValue('contacts/',8);
        if ((season)%4 == 1) {   // spring time
                        planting = plantingCount * 0.1;
                        await updatee('contact/', 10, { value: planting }); // update seeds planted
                        let plantedcount = await getValue('contacts/',10);
                        document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);
                    }
        else if ((season)%4 == 3) {  // fall            
                    harvesting = 0.1 * plantingCount;
                    let toAdd = 0;
                    await updatee('contact/', 10, {value: -1 * harvesting}) // less seeds currently planted
                        /// check if this is < 0
                    left = await getValue('contacts/',10);
                    if (left < 0) {
                        toAdd = left
                    }
                    await updatee('contact/',10, {value: -toAdd})
                    await updatee('resources/',2, {value : harvesting + toAdd}) //change wheat values;

                    let plantedcount = await getValue('contacts/',10);
                    document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);
         } else if ((season)%4 == 0) {    //winter
                await setVal('contact/', 10, { value: 0 }) //////////////
                document.getElementById('Planted').innerText = 0;
        }
    }

async function advanceCooks() {
    let toAdd = 0;
    let cookers = await getValue('contacts/',3);
    cookingPower = cookers * 0.1;
    await updatee('resources/', 2, {value: -1 * cookingPower}) // takes out wheat
    left = await getValue('resources/',2);  // this is the value of the wheat that we have
    if (left < 0) {
        toAdd = left
    }       // toAdd back up bc you can't have negative resources
    await updatee('resources/',2, {value: -toAdd})  //wheat moves back to 0
    await updatee('resources/',6, {value : cookingPower + toAdd}) //change bread values;   

    
}

async function advanceHunters() {
    let hunting = await getValue('contacts/', 2)
    change = hunting * 0.1;                             // make this random based on luck
    await updatee('resources/', 3, { value: change }) // fur
    await updatee('resources/', 4, { value: change }) // raw meat

}