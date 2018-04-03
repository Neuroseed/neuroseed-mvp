import metadata

CONV2D_LAY = {
    "type": "object",
    "properties":{
        "name":{
            "type": "string",
            "pattern": "^Conv2D$"
        },
        "config":{
            "type": "object",
            "properties":{
                "filters": {
                    "type": "integer",
                },
                "kernel_size":{
                    "type": "array",
                    "minItems": 1,
                    "items":{
                        "type": "integer",
                    },
                },
                "strides":{
                    "type": "array",
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                    },
                },
                "padding":{
                    "type": "string",
                },
                "dilation_rate":{
                    "type": "array",
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                    }
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
            "required": ["filters", "kernel_size"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
