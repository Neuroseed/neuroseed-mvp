import metadata

DENSE_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Dense$"
                },
        "config":{
            "type": "object",
            "properties":{
                "units": {
                    "type": "integer",
                },
                "activation":{
                    "type": "string",
                },
                "use_bias":{
                    "type": "boolean",
                },
                "kernel_initializer":{
                    "type": "string",
                },
                "bias_initializer":{
                    "type": "string",
                },
                "kernel_regularizer":{
                    "type": "string",
                },
                "bias_regularizer":{
                    "type": "string",
                },
                "activity_regularizer":{
                    "type": "string",
                },
                "kernel_constraint":{
                    "type": "string",
                },
                "bias_constraint":{
                    "type": "string",
                },
            },
            "required": ["units"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
