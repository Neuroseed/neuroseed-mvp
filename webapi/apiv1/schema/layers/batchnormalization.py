import metadata
from .constants import *

BATCHNORMALIZATION_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^BatchNormalization$"
        },
        "config": {
            "type": "object",
            "properties": {
                "axis": {
                    "type": "integer",
                    "minimum": -100000,
                    "maximum": 100000,
                },
                "momentum": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "epsilon": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "center": {
                    "type": "boolean",
                },
                "scale": {
                    "type": "boolean",
                },
                "beta_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "gamma_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "moving_mean_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "moving_variance_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "beta_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "gamma_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "beta_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
                "gamma_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
            },
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
