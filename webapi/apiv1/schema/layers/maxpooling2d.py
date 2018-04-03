import metadata

MAXPOOLING2D_LAY = {
    "type": "object",
    "properties":{
        "name":{
            "type": "string",
            "pattern": "^Maxpooling2d$"
        },
        "config":{
            "type": "object",
            "properties":{
                "pool_size": {
                    "type": "array",
                    "maxItems": 2,
                    "items":{
                        "type": "integer",
                    },
                },
                "strides":{
                    "type": "array",
                    "minItems": 2,
                    "items":{
                        "type": "integer",
                    },
                },
                "padding":{
                    "type": "string",
                },
                "data_format":{
                    "type": "string",
                },
            },
        },
    },
}
