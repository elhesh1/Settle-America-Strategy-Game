


initial_variables = [
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Farmers", "efficiency" :  { "e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Hunters",  "efficiency" : {"e": 0.025, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Cooks",  "efficiency" : {"e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Loggers",  "efficiency" : {"e": 0.1, "season" : {0:0.6, 1:0.95, 2:1, 3:1 }}},
        {"value" : 50, "maximum": 2147483647, "minimum": 0, "type": "NOT", "name" : "Population"},
        {"value" : 50, "maximum": 10, "minimum": 0, "type": "NOT", "name" : "Avaliable"},
        {"value" : 1, "maximum" : 2147483647, "minimum": 0, "type" : "NOT", "name" : "Week"},
        {"value" : 1, "maximum" : 9999999, "minimum": 0, "type" : "NOT", "name" : "Season"},
        {"value" : 1620, "maximum" : 2147483647, "minimum": 0, "type" : "RES", "name" : "Year"},
        {"value" : 0, "maximum" : 2147483647, "minimum": -999999, "type" : "RES", "name" : "Planted"},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Butchers", "efficiency" : { "e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 100, "maximum": 101, "minimum": 0, "type" : "NOT", "name" : "RationP" },
        {"value": 85, "maximum": 100, "minimum":0,  "type" : "NOT", "name" : "Health"},
        {"value": 1, "maximum":2147483647, "minimum":1, "type" : "NOT", "name" : "JobAddModifier"}, ## error with this perhaps
        {"value" : 0 , "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Builders", "efficiency" : { "e": 0.1, "season" : {0:6, 1:1, 2:1, 3:1 }}},
        {"value" : 1, "maximum" : 2187442145, "minimum" : 1, "type" : "NOT", "name" : "queueIndex" },
        {"value" : 4, "maximum" : 2187442145, "minimum" : 0, "type" : "NOT", "name" : "numberofFoods" },
        {"value" : 92.5, "maximum" : 2187442145, "minimum" : 0, "type" : "NOT", "name" : "Strength" }, #18 
        {"value" : -1, "maximum" : 99999999, "minimum" : 0, "name" : "SupplyTime"},
        {"value" : 0, "maximum" : 99999999, "minimum" : 0, "name" : "SupplyShipsGiven"},
        {"value" : 0, "name" : "SupplyShipType"}

    ]

initial_resources = [
        {"value": 0, "name" : "Seeds", "always" : 1 },
        {"value": 0, "name" : "Wheat"  },
        {"value": 0,  "name" : "Fur"}, 
        {"value": 0,  "name" : "Raw Meat"},
        {"value": 0, "name" : "Wood"},
        {"value": 16, "name" : "Bread"},
        {"value": 4, "name" : "Cooked Meat"},
        {"value": 0, "name" : "Wild Berries"},
        {"value" : 4, "name" : "Vegtables"},
        {"value" : 10, "name" : "Iron Hoe",'integer' : 1},
        {"value" : 20, "name" : "Iron Sickle", 'integer' : 1},
        {"value" : 10, "name" : "Iron Axe", 'integer' : 1}, 
        {"value" : 5, "name" : "Rifle", 'integer' : 1}, 
        {"value" : 10, "name" : "Bow", 'integer' : 1}, 
        {"value" : 10, "name" : "Iron Shovel", 'integer' : 1}, #15
        {"value" : 8, "name" : "Iron Pickaxe", 'integer' : 1}, 
        {"value" : 0, "name" : "Clay", "always" : 1 },
        {"value" : 0, "name" :"Iron Ore", "always" : 1 },
        {"value" : 0, "name" : "People", "always" : 1, "integer" : 1}

]

# init values

initial_buildings = [ # - work means building is special
        {"value": 0, "name" : "LogCabin", "work" : 1, "cost" : {"5": 1}, "capacity" : 5, "fullname" : "Log Cabin", "typeOfBuilding" : "Housing"},
        {"value": 1, "name" : "TownHall", "work" : -1, "cost" : -1, "fullname" : "Town Hall"},
        {"value": 5, "name" : "ClayPit", "work" : 0.1, "cost" : {"5": 0.2},  "capacity" : 5, "fullname" : "Clay Pit", "typeOfBuilding" : "Raw Material Maker", "working" : {"value" : 0, "maximum" : 20, "minimum" : 0},
         "tools" : {"None" : 0.5, "With" : [15,1], "Base" : 0.1}, "Inputs" : {}, "Outputs" : {"17" : 1}},
       {"value": 5, "name" : "Mine", "work" : 0.3, "cost" : {"4": 0.5},  "capacity" : 4, "fullname" : "Mine", "typeOfBuilding" : "Raw Material Maker", "working" : {"value" : 0, "maximum" : 20, "minimum" : 0},
        "tools" : {"None" : 0.3, "With" : [16,1.1], "Base" : 0.1}, "Inputs" : {}, "Outputs" : {"18" : 1} }


]

currently_building = []