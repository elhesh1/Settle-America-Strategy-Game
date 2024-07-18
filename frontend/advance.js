function advance() {
    updatee(7,{value : 1})
    .then(() => {                           // retrieves val from db
        getValue(7)            
            .then(value => {
                if (value == 14) {
                    value = 1;
                    updatee(7,{value : -13});
                } 
                document.getElementById("W").innerText = value;    // pastes that bad boy in
                
            })
    })

}

// function season(value) {
//     if ((value-1)%13 == 0) {
//         console.log("NEW SEASON,  " , value);
//     }
// }
