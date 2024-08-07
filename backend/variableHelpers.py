


initial_variables = [
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Farmers", "efficiency" :  {"e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Hunters",  "efficiency" : {"e": 0.025, "season" : {0:6, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Cooks",  "efficiency" : {"e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Loggers",  "efficiency" : {"e": 0.1, "season" : {0:0.6, 1:0.95, 2:1, 3:1 }}},
        {"value" : 50, "maximum": 2147483647, "minimum": 0, "type": "NOT", "name" : "Population"},
        {"value" : 50, "maximum": 10, "minimum": 0, "type": "NOT", "name" : "Avaliable"},
        {"value" : 1, "maximum" : 2147483647, "minimum": 0, "type" : "NOT", "name" : "Week"},
        {"value" : 1, "maximum" : 9999999, "minimum": 0, "type" : "NOT", "name" : "Season"},
        {"value" : 0, "maximum" : 2147483647, "minimum": 0, "type" : "RES", "name" : "Year"},
        {"value" : 0, "maximum" : 2147483647, "minimum": -999999, "type" : "RES", "name" : "Planted"},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Butchers", "efficiency" : {"e": 0.1, "season" : {0:1, 1:1, 2:1, 3:1 }}},
        {"value": 100, "maximum": 101, "minimum": 0, "type" : "NOT", "name" : "RationP" },
        {"value": 100, "maximum": 100, "minimum":0,  "type" : "NOT", "name" : "Health"},
        {"value": 1, "maximum":2147483647, "minimum":1, "type" : "NOT", "name" : "JobAddModifier"}, ## error with this perhaps
        {"value" : 0 , "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Builders", "efficiency" : {"e": 0.1, "season" : {0:6, 1:1, 2:1, 3:1 }}},
        {"value" : 1, "maximum" : 2187442145, "minimum" : 1, "type" : "NOT", "name" : "queueIndex" },
        {"value" : 4, "maximum" : 2187442145, "minimum" : 0, "type" : "NOT", "name" : "numberofFoods" }

    ]

initial_resources = [
        {"value": 0, "name" : "Seeds"},
        {"value": 0, "name" : "Wheat" , "cook" : 1},
        {"value": 0,  "name" : "Fur"},
        {"value": 0,  "name" : "Raw Meat", "cook":1}, 
        {"value": 0, "name" : "Wood"},
        {"value": 10, "name" : "Bread"},
        {"value": 10, "name" : "Cooked Meat"},
        {"value": 2, "name" : "Wild Berries"},
        {"value" : 4, "name" : "Vegtables"}
]

initial_buildings = [
        {"value": 0, "name" : "LogCabins", "work" : 1, "cost" : {"5": 1}, "capacity" : 4}
]

currently_building = []