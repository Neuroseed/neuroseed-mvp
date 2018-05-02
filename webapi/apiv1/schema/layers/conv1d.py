import metadata
from .constants import *

CONV1D_LAY = {
    "type": "object",
    "title": "Conv1D",
    "description": "1D convolution layer",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Conv1D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Conv1D"
        },
        "config": {
            "type": "object",
            "properties": {
                "filters": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 1000,
                    "title": "Filters",
                    "description": "Number of convolution filters",
                    "default": 32
                },
                "kernel_size": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 1000,
                    "title": "Kernel size",
                    "description": "An integer, specifying the length of the 1D convolution window.",
                    "default": 2
                },
                "strides": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                    "title": "Strides",
                    "description": "An integer specifying the stride length of the convolution",
                    "default": 1
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING,
                    "title": "Padding",
                    "default": "valid"
                },
                "dilation_rate": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                    "title": "Dilation rate",
                    "default": 1
                },
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS,
                    "title": "Activation",
                    "default": "linear"
                },
                "use_bias": {
                    "type": "boolean",
                    "title": "Use bias",
                    "default": True
                },
                # "kernel_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "bias_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "kernel_regularizer": {
                #     "type": "string",
                #      "enum": REGULARIZERS
                # },
                # "bias_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS
                # },
                # "activity_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS
                # },
                # "kernel_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
                # "bias_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
            },
            "required": ["filters", "kernel_size"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
