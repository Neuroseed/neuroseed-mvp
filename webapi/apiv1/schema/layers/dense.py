import metadata
from .constants import ACTIVATIONS

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
                    "minimum": 1,
                    "maximum": 10000,
                    "type": "integer",
                },
                "activation":{
                    "type": "string",
                    "enum": ACTIVATIONS
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
            "required": ["units"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
