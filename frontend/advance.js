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
                document.getElementById("W").innerText = value; 
               
            advanceJob()
            .then(() => {
                console.log("Logging and updating resources completed successfully.");
                tableMaker(); 
            })
   

            })
    })
}

function advanceJob() {
    return advanceLoggers()
 
}

function advanceLoggers() {
    return getValue('contacts/', 4)
    .then(value => {
        console.log("Logging:", value);
        woodChange = value * 0.1;
        return updatee('resources/', 5, { value: woodChange });
    })
}
