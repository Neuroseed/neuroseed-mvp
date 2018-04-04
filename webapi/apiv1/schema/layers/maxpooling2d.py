import metadata

MAXPOOLING2D_LAY = {
    "type": "object",
    "properties":{
        "name":{
            "type": "string",
            "pattern": "^MaxPooling2D$"
        },
        "config":{
            "type": "object",
            "properties":{
                "pool_size": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items":{
                        "type": "integer",
                    },
                },
                "strides":{
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items":{
                        "type": "integer",
                    },
                },
                "padding":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "data_format":{
                    "minLength": 6,
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
