async function advance() {
    var weak = 0;
    await advanceJob();              // do jobs
    updatee('contact/',7,{value : 1})
    .then(() => {                           // retrieves val from db
        getValue('contacts/',7)
        .then(value => {
                weak = value;
                console.log(value);
            })
                                            // change weeks
            .then(() => {
                value = weak;
                if (value == 14) { //       NEW SEASON
                    value = 1;
                    updatee('contact/', 7,{value : -13});
                    getValue('contacts/',8)
                    .then(value => {  //gets season val
                        console.log("NEW SEASON   ", value);
                        switch((value + 1)%4) {
                            case 1:
                                document.getElementById("Season").textContent = "Spring"; break;
                            case 2:
                                document.getElementById("Season").textContent = "Summer";  break; 
                            case 3:
                                document.getElementById("Season").textContent = "Fall"; break;
                            case 0:
                                document.getElementById("Season").textContent = "Winter"; break;
                        }
                        updatee('contact/',8, {value : 1}); 
                        

                    })
                } 
                document.getElementById("W").innerText = value; 
            

            })
    })
}

async function advanceJob() {
   await advanceLoggers();
   await advancePlanters();
   tableMaker();
 
 
}




async function advanceLoggers() {
    let logging = await getValue('contacts/', 4)
    woodChange = logging * 0.1;
    await updatee('resources/', 5, { value: woodChange })
        
}

async function advancePlanters() {

        let plantingCount = await getValue('contacts/', 1);
        console.log(plantingCount);
        let season = await getValue('contacts/',8);
        if ((season)%4 == 1) {   // spring time
                        console.log("Planting:", plantingCount);
                        planting = plantingCount * 0.1;
                        await updatee('contact/', 10, { value: planting }); // update seeds planted
                        let plantedcount = await getValue('contacts/',10);
                        document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);
                    }
        else if ((season)%4 == 3) {  // fall            /// MAKE IT CHECK IF OVERFLOW BRUH BRUH BRUH BRUH BRUH BRUH BRUH BRUH BRUH BRUH BRUH
                    console.log("FALL  ", plantingCount);
                    harvesting = 0.1 * plantingCount;
                    let toAdd = 0;
                    await updatee('contact/', 10, {value: -1 * harvesting}) // less seeds currently planted
                        /// check if this is < 0
                    left = await getValue('contacts/',10);
                    console.log("value left dog  ", left);
                    if (left < 0) {
                        toAdd = left
                    }
                    await updatee('contact/',10, {value: -toAdd})
                    await updatee('resources/',2, {value : harvesting + toAdd}) //change wheat values;

                    let plantedcount = await getValue('contacts/',10);
                    document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);
         } else if ((season)%4 == 0) {    //winter
                await updatee('contact/', 10, { value: -999999999 })
                document.getElementById('Planted').innerText = 0;

        }
    }