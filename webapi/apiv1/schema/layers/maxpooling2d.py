import metadata

MAXPOOLING2D_LAY = {
    "type": "object",
    "properties":{
        "name":{
            "type": "string",
            "pattern": "^Maxpooling2D$"
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
                    "maxLength": 16,
                    "type": "string",
                },
                "data_format":{
                    "maxLength": 16,
                    "type": "string",
                },
            },
            "required": ["pool_size"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
