from .constants import *

DENSE_LAY = {
    "type": "object",
    "title": "Dense",
    "description": "Densely-connected layer",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Dense$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Dense"
        },
        "config": {
            "type": "object",
            "properties": {
                "units": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10000,
                    "title": "Units",
                    "description": "Number of neurons",
                    "default": 1
                },
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS,
                    "title": "Activation function",
                    "description": "Activation function for layer",
                    "default": "linear"
                },
                "use_bias": {
                    "type": "boolean",
                    "title": "Use bias",
                    "description": "Use bias in layer",
                    "default": True
                },
                "kernel_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS,
                    "title": "Kernel initializer",
                    "default": None
                },
                "bias_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS,
                    "title": "Bias initializer",
                    "default": None
                },
                "kernel_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS,
                    "title": "Kernel regularizer",
                    "default": None
                },
                "bias_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS,
                    "title": "Bias regularizer",
                    "default": None
                },
                "activity_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS,
                    "title": "Activity regularizer",
                    "default": None
                },
                "kernel_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS,
                    "title": "Kernel constraint",
                    "default": None
                },
                "bias_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS,
                    "title": "Bias constraint",
                    "default": None
                },
            },
            "required": ["units"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
