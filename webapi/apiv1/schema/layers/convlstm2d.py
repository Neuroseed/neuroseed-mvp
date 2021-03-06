from .constants import *

CONVLSTM2D_LAY = {
    "type": "object",
    "title": "Conv2D",
    "description": "2D convolution layer",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^ConvLSTM2D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "ConvLSTM2D"
        },
        "config": {
            "type": "object",
            "properties": {
                "filters": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 2**14,
                    "title": "Filters",
                    "description": "Number of convolution filters",
                    "default": 32
                },
                "kernel_size": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 128
                    },
                    "title": "Kernel size",
                    "description": "List of 2 integers specifying the width and height of the 2D convolution window",
                    "default": [2, 2]
                },
                "strides": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 128
                    },
                    "title": "Strides",
                    "description": "List of 2 integers specifying the strides of the convolution along the width and height",
                    "default": [2, 2]
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING,
                    "title": "Padding",
                    "default": "valid"
                },
                "dilation_rate": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 128
                    },
                    "title": "Dilation rate",
                    "default": [2, 2]
                },
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS,
                    "title": "Activation",
                    "default": "linear"
                },
                "recurrent_activation": {
                    "type": "string",
                    "enum": ACTIVATIONS
                },
                "use_bias": {
                    "type": "boolean",
                    "title": "Use bias",
                    "default": True
                },
                # "kernel_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS,
                #     "title": "Kernel initializer",
                #     "default": None
                # },
                # "recurrent_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS,
                #     "title": "Kernel initializer",
                #     "default": None
                # },
                # "bias_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS,
                #     "title": "Bias initializer",
                #     "default": None
                # },
                # "unit_forget_bias": {
                #    "type": "boolean",
                #    "title": "Units forget bias",
                #    "default": True
                # },
                # "kernel_regularizer": {
                #     "type": "string",
                #      "enum": REGULARIZERS,
                #     "title": "Kernel regularizer",
                #     "default": None
                # },
                # "recurrent_regularizer": {
                #     "type": "string",
                #      "enum": REGULARIZERS,
                #     "title": "Recurrent regularizer",
                #     "default": None
                # },
                # "bias_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS,
                #     "title": "Bias regularizer",
                #     "default": None
                # },
                # "activity_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS,
                #     "title": "Activity regularizer",
                #     "default": None
                # },
                # "kernel_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS,
                #     "title": "Kernel constraint",
                #     "default": None
                # },
                # "recurrent_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS,
                #     "title": "Kernel constraint",
                #     "default": None
                # },
                # "bias_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS,
                #     "title": "Bias constraint",
                #     "default": None
                # },
                # "return_sequences": {
                #     "type": "boolean",
                # },
                # "go_backwards": {
                #     "type": "boolean",
                # },
                # "statefull": {
                #     "type": "boolean",
                # },
                # "dropout": {
                #    "type": "number",
                #    "minimum": 0,
                #    "maximum": 1,
                # },
                # "recurrent_dropout": {
                #    "type": "number",
                #   "minimum": 0,
                #    "maximum": 1,
                # },
            },
            "required": ["filters", "kernel_size"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
