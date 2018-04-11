import metadata
from .constants import *

DENSE_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Dense$"
                },
        "config": {
            "type": "object",
            "properties": {
                "units": {
                    "minimum": 1,
                    "maximum": 10000,
                    "type": "integer",
                },
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS
                },
                "use_bias": {
                    "type": "boolean",
                },
                "kernel_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "bias_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "kernel_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "bias_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "activity_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "kernel_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
                "bias_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
            },
            "required": ["units"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
