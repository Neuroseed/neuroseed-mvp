import metadata
from .constants import *

CONV1D_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Conv1D$"
        },
        "config": {
            "type": "object",
            "properties": {
                "filters": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 1000,
                },
                "kernel_size": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {
                        "type": "integer",
                    },
                },
                "strides": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {
                        "type": "integer",
                    },
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING
                },
                "dilation_rate": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {
                        "type": "integer",
                    }
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
            "required": ["filters", "kernel_size"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
