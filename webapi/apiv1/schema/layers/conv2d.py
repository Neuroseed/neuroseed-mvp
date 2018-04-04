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
                    "items": {
                        "type": "integer",
                    },
                },
                "padding":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "dilation_rate":{
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                    }
                },
                "activation":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "use_bias":{
                    "type": "boolean",
                },
                "kernel_initializer":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_initializer":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "kernel_regularizer":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_regularizer":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "activity_regularizer":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "kernel_constraint":{
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
                "bias_constraint":{
                    "minLength": 6,
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
