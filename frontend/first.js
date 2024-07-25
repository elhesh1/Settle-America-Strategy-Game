
window.onload = function() {
   setGame();
}

function setGame() { // this sets up all the functions

    const buttons = document.querySelectorAll('.B');                // + and - buttons for jobs
        buttons.forEach(button => {
        button.addEventListener('click', buttonAction);
    });
    reset.addEventListener('click', resett);

    const nextW = document.getElementById('NextW');                // Advance button    
    nextW.addEventListener('click', async function() {
        nextW.disabled = true; 
        try {
            await advance(); 
        } catch (error) {
            console.error('Error:', error);
        } finally {
            nextW.disabled = false; 
        }
    });
    document.getElementById('InventoryT').click();      //Tab buttons declared in html  // sets up as inventory
    const AdjustB = document.querySelectorAll('.Adjust');
        AdjustB.forEach(AdjB => {
            AdjB.addEventListener('click',changeValueOfInputForJobs);
        });

    document.getElementById('Clear').addEventListener('click', clearJobs);


}

function buttonAction() { 
    id = this.id
    var jobID = buttonMap[id][0]
    var type = labelMap[jobID][0]

    updatee('contact/', jobID, {value: buttonMap[id][1]}) // updates in db
    .then(() => {                           // retrieves val from db
        getValue('contacts/',jobID)
            .then(value => {
                document.getElementById(type).innerText = value;    // pastes that bad boy in
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById(type).innerText = 'Error fetching data';
            });
        getValue('contacts/',6)
            .then(value => {
                document.getElementById('A').innerText = value;
            })
            .catch(error => {
                console.error('Error fetching data for jobID 6:', error);
                document.getElementById('A').innerText = 'Error fetching data';
            });
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });

}

function resett() {     // function from resett it is used 
    document.getElementById("Season").textContent = "Spring";
    document.getElementById('One').click();
    resettHelper()
    .then(() => {
        Object.keys(labelMap).forEach(key => {
            getValue('contacts/',key) 
            .then(value => {
                document.getElementById(labelMap[key][0]).innerText = value;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById(labelMap[key][0]).innerText = 'Error fetching data';
            });
        });
    })
    .then(() => {
        tableMaker();
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });
}

async function resettHelper() {
    try {
         const response = await fetch('http://127.0.0.1:5000/reset', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });
            const responseData = await response.json();
        }
        catch (error) {       // did not work
            console.error('Error:', error);
        }
}

async function getValue(type,user_id) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/${type}${user_id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.value;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}



async function updatee(type, user_id, options) {
    
    const data = {};

    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    // set up data yk

     try {      // try to patch that john
        const response = await fetch(`http://127.0.0.1:5000/update_${type}${user_id}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });


        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();

    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}


function openTab(id, value) {
    tabcontent = document.getElementsByClassName("tabcontent"); // hid all other Tabs doggg
    for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
    }
    document.getElementById(value).style.display = "grid"


    tabB = document.getElementsByClassName("tabB");
    for (i = 0; i < tabB.length; i++) {
        tabB[i].className = tabB[i].className.replace(" active", "");
    }
    thisdude = document.getElementById(id);
    thisdude.className += " active";
}

async function setVal(type, user_id, options) {
    const data = {};
    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    try {     
        const response = await fetch(`http://127.0.0.1:5000/set_${type}${user_id}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });
        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const responseData = await response.json();
    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}

async function foodParagraphHelper() {
    let pop = await getValue('contacts/',5)
    return "Every citizen needs 0.02 food a week to be fully fed. With a population of " + pop + ", " + pop*0.02 + " food is needed every week to keep them at full strength";

}

function foodParagraph() {
   foodParagraphHelper()
   .then(iv => {
        foodpopcontainer.innerHTML = iv; 
    })
    .catch(error => {
    console.error("Error in tester:", error);
    });
}

function changeValueOfInputForJobs() {
    id = this.id
    setVal('contact/',14, {value: jobMulti[id] } )

    const AdjustB = document.querySelectorAll('.Adjust');
        AdjustB.forEach(AdjB => {
            AdjB.className = AdjB.className.replace(" active", "");
    });

    thisdude = document.getElementById(id);
    thisdude.className += " active";

    return 
}

async function clearJobs() {
    const response = await fetch(`http://127.0.0.1:5000/clearJobs`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),  
    })
        for (let key in labelMap) {
            if( labelMap[key][1] == "JOB") {
                jobb = document.getElementById(labelMap[key][0]);
                jobb.innerText = 0;
            }
        }

    let av = await getValue('contacts/',6)
    aval = document.getElementById('A');
    aval.innerText = av
}