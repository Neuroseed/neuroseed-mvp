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
                    "maxLength": 16,
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
                    "maxLength": 16,
                    "type": "string",
                },
                "use_bias":{
                    "type": "boolean",
                },
                "kernel_initializer":{
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_initializer":{
                    "maxLength": 16,
                    "type": "string",
                },
                "kernel_regularizer":{
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_regularizer":{
                    "maxLength": 16,
                    "type": "string",
                },
                "activity_regularizer":{
                    "maxLength": 16,
                    "type": "string",
                },
                "kernel_constraint":{
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_constraint":{
                    "maxLength": 16,
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
