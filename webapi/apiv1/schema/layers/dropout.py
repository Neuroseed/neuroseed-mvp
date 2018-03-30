import metadata

DROPOUT_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Dropout$"
        },
        "config":{
            "type": "object",
            "properties":{
                "rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "noise_shape":{
                    "type": "array",
                    "minItems": 1,
                    "items":{
                        "type": "integer",
                    },
                },
                "seed":{
                    "type": "array",
                    "minItems": 1,
                    "items":{
                        "type": "integer",
                    },
                },
            },
        },
    },
}
