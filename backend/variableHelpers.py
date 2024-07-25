


initial_variables = [
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Farmers", },
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Hunters"},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Cooks"},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB", "name" : "Loggers"},
        {"value" : 50, "maximum": 2147483647, "minimum": 0, "type": "NOT", "name" : "Population"},
        {"value" : 40, "maximum": 10, "minimum": 0, "type": "NOT", "name" : "Avaliable"},
        {"value" : 1, "maximum" : 2147483647, "minimum": 0, "type" : "NOT", "name" : "Week"},
        {"value" : 1, "maximum" : 9999999, "minimum": 0, "type" : "NOT", "name" : "Season"},
        {"value" : 0, "maximum" : 2147483647, "minimum": 0, "type" : "RES", "name" : "Year"},
        {"value" : 0, "maximum" : 2147483647, "minimum": -999999, "type" : "RES", "name" : "Planted"},
        {"value": 0, "maximum": 2147483647, "minimum": 0, "type": "JOB",  "name" : "Butchers", },
        {"value": 100, "maximum": 101, "minimum": 0, "type" : "NOT", "name" : "RationP" },
        {"value": 100, "maximum": 100, "minimum":0,  "type" : "NOT", "name" : "Health"},
        {"value": 1, "maximum":2147483647, "minimum":1, "type" : "NOT", "name" : "JobAddModifier"},

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