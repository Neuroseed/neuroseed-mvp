import metadata
from .constants import *

GRU_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^GRU$"
        },
        "config": {
            "type": "object",
            "properties": {
                "units": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                },
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS
                },
                "recurent_activation": {
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
                "recurrent_initializer": {
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
                "recurrent_regularizer":{
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
                "recurrent_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
                "bias_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
                "dropout": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "recurrent_dropout": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "implementation": {
                    "type": "integer",
                    "enum": INTEGERS
                },
                "return_sequences": {
                    "type": "boolean",
                },
                "return_state": {
                    "type": "boolean",
                },
                "go_backwards": {
                    "type": "boolean",
                },
                "statefull": {
                    "type": "boolean",
                },
                "unroll": {
                    "type": "boolean",
                },
                "restart_after": {
                    "type": "boolean",
                },
            },
            "required": ["units"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
