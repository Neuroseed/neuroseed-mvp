import metadata
from .constants import *

SIMPLERNN_LAY = {
    "type": "object",
    "title": "SimpleRNN",
    "description": "Fully-connected RNN where the output is to be fed back to input",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^SimpleRNN$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "SimpleRNN"
        },
        "config": {
            "type": "object",
            "properties": {
                "units": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
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
                # "kernel_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "recurrent_initializer": {
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
                # "recurrent_regularizer":{
                #     "type": "string",
                #     "enum": REGULARIZERS
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
                # "recurrent_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
                # "bias_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
                "dropout": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Dropout",
                    "description": "Fraction of the units to drop for the linear transformation of the inputs.",
                    "default": 0
                },
                "recurrent_dropout": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Implementation",
                    "description": "Implementation mode, either 1 or 2. Mode 1 will structure its operations as a larger number of smaller dot products and additions, whereas mode 2 will batch them into fewer, larger operations.",
                    "default": 1
                },
                "return_sequences": {
                    "type": "boolean",
                    "title": "Return sequences",
                    "description": "Whether to return the last output in the output sequence, or the full sequence.",
                    "default": False
                },
                "return_state": {
                    "type": "boolean",
                    "title": "Return state",
                    "description": "Whether to return the last state in addition to the output.",
                    "default": False
                },
                "go_backwards": {
                    "type": "boolean",
                    "title": "Go backwards",
                    "description": "If True, process the input sequence backwards and return the reversed sequence.",
                    "default": False
                },
                "statefull": {
                    "type": "boolean",
                    "title": "Statefull",
                    "description": " If True, the last state for each sample at index i in a batch will be used as initial state for the sample of index i in the following batch.",
                    "default": False
                },
                "unroll": {
                    "type": "boolean",
                    "title": "Unroll",
                    "description": "If True, the network will be unrolled, else a symbolic loop will be used. Unrolling can speed-up a RNN, although it tends to be more memory-intensive. Unrolling is only suitable for short sequences.",
                    "default": False
                },
            },
            "required": ["units"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
