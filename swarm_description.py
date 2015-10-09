SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
    {
      "fieldName": "tempvariation",
      "fieldType": "float",
      "maxValue": 30,
      "minValue": 0
    },
    {
      "fieldName": "hail",
      "fieldType": "int",
      "maxValue": 1,
      "minValue": 0
    },
    {
      "fieldName": "meanwindspdm",
      "fieldType": "int",
      "maxValue": 80,
      "minValue": 0
    },
    {
      "fieldName": "precip",
      "fieldType": "float",
      "maxValue": 50.0,
      "minValue": 0.0
    },
    {
      "fieldName": "debris",
      "fieldType": "int",
      "maxValue": 600,
      "minValue": 0
    }
  ],
  "streamDef": {
    "info": "debris",
    "version": 1,
    "streams": [
      {
        "info": "Weather Tree Debris",
        "source": "file://weather_debris_data.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "debris"
  },
  "iterationCount": -1,
  "swarmSize": "medium"
}
