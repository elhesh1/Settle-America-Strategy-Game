const labelMap = {// labels but also add type
    1 : ['F','JOB','FarmerJobGrid'],
    2 : ['H','JOB','HuntersJobGrid'],
    3 : ['C','JOB','CooksJobGrid'],
    4 : ['L','JOB','LoggersJobGrid'],
    5 : ['P','NOT'],
    6 : ['A','NOT'],
    7 : ['W','NOT'], 
    11 : ['B', 'JOB','ButchersJobGrid'],
    15 : ['W2', 'JOB','BuilderJobGrid'],   
}

const jobMulti = {
    "One" : 1,
    "Ten" : 10,
    "Hundred" : 100,
    "Max" : 2147483647
}


const buildingNames = {} // id to Name. This is set up automatically 
const namesBuilding = {} // fullname -> array with first element ID

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

const BuildingIDs = { // Name : [ name, building, value-changer ] // value changer not even needed fr
 
    xMU : ['xCM', 2 ,1],
    xTU : ['xCT',7,1],
    xMD : ['xCM' , 2 ,-1],
}

const BuildingShown = {
    2 : 'xAM',
}

