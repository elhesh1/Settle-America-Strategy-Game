
async function advance() {              //////////////// THIS FUNCTION TAKES 25 AWAITS.. MOVE TO BACKEND SO IT WILL BE FASTER DOG  7/23 
    await advanceJob();              // do jobs
    let w = await getValue('contacts/', 7)
    document.getElementById("W").textContent = w;
    if(w == 1) {
        let s = await getValue('contacts/',8);
        switch(s) {
            case 1:
                document.getElementById("Season").textContent = "Spring"; break;
            case 2:
                document.getElementById("Season").textContent = "Summer";  break; 
            case 3:
                document.getElementById("Season").textContent = "Fall"; break;
            case 0:
                document.getElementById("Season").textContent = "Winter"; 
                let y = await getValue('contacts/',9);
                document.getElementById("Year").textContent = y; 
                break;

        }


    }
    let val = await getValue('contacts/',13);
    console.log(val);
    document.getElementById("HealthN").innerText = val; 
    let population = await getValue('contacts/',5)
    document.getElementById("P").textContent = population

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

    tableMaker();
 
 
}