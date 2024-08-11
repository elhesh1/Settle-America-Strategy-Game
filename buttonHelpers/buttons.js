const buttonMap = { // Name : [ name, value-changer ]
    BFU : [1, 1],
    BFD : [1, -1],
    BHU : [2, 1], 
    BHD : [2, -1],
    BCU : [3, 1],
    BCD : [3, -1],
    BLU : [4, 1],
    BLD : [4, -1], 
    BBU : [11,1],
    BBD : [11,-1],
    WCU : [15 , 1],
    WCD : [15 , -1] 
};

const BuildingIDs = { // Name : [ name, building, value-changer ]
    xLU : ['xCL', 1 ,1],
    xLD : ['xCL' , 1 ,-1],
    xMU : ['xCM', 2 ,1],
    xMD : ['xCM' , 2 ,-1],
}

const BuildingShown = {
    1 : 'xAL',
    2 : 'xAM',
}

const buildingNames = {
    1 : "Log Cabin",
    2 : "Mine",

}
