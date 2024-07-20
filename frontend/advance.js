function advance() {
    updatee('contact/',7,{value : 1})
    .then(() => {                           // retrieves val from db
        getValue('contacts/',7)            
            .then(value => {
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
                document.getElementById("W").innerText = value;    // pastes that bad boy in
               
            advanceJob()
            .then(() => {
                //console.log(document.getElementById)
                if (document.getElementById('InventoryT').classList.contains('active')) {
                    tableMaker();
                } 
            })    

            })
    })
}

async function advanceJob() {       // these functions may not work as inteneded so try that shit
    advanceLoggers()
    .then(()=> {
        console.log("I think I moved the loggers but idk  ");
        // do other stuff

    })

}


async function advanceLoggers() {
    try {
    getValue('contacts/',4)
    .then(value => {
        console.log(" Logging  ", value);
        woodChange = value * 0.1;
        updatee('resources/',5, {value : woodChange});



    })
    } catch (error){}

}
