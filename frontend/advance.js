
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
    let plantedcount = await getValue('contacts/',10);
    document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);//////////////////////////////////////////////////////////////////////


    await setVal('contact/', 12, {value : parseInt(document.getElementById("sliderValue").textContent)})
    let val = await getValue('contacts/',13);
    console.log(val);
    document.getElementById("HealthN").innerText = val; 
    tableMaker();
 
 
}

