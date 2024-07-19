function advance() {
    updatee(7,{value : 1})
    .then(() => {                           // retrieves val from db
        getValue(7)            
            .then(value => {
                if (value == 14) { //       NEW SEASON
                    value = 1;
                    updatee(7,{value : -13});
                    getValue(12)
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
                        updatee(12, {value : 1}); 


                    })
                } 
                document.getElementById("W").innerText = value;    // pastes that bad boy in
                
            })
    })

}


