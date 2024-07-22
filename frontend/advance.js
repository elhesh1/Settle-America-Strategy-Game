
async function advance() {              //////////////// THIS FUNCTION TAKES 25 AWAITS.. MOVE TO BACKEND SO IT WILL BE FASTER DOG  7/23 
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
    const response = await fetch(`http://127.0.0.1:5000/advance`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify([]),  
    });

    await advanceLoggers();
    await advancePlanters();
    await setVal('contact/', 12, {value : parseInt(document.getElementById("sliderValue").textContent)})
    await eat();
    tableMaker();
 
 
}


async function eat() {
    try {      // try to patch that john
        const response = await fetch(`http://127.0.0.1:5000/eat`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify([]),  
        });
    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
    let val = await getValue('contacts/',13);
    console.log(val);
    document.getElementById("HealthN").innerText = val; 
    return


}

async function advanceLoggers() {
    let logging = await getValue('contacts/', 4)
    woodChange = logging * 0.1;
    await updatee('resources/', 5, { value: woodChange })
        
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

