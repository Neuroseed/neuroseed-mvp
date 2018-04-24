import metadata
from .constants import *

BATCHNORMALIZATION_LAY = {
    "type": "object",
    "title": "BatchNormalization",
    "description": "Batch normalization layer",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^BatchNormalization$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "BatchNormalization"
        },
        "config": {
            "type": "object",
            "properties": {
                "axis": {
                    "type": "integer",
                    "minimum": -10,
                    "maximum": 10,
                    "title": "Axis",
                    "default": -1
                },
                "momentum": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Momentum",
                    "default": 0.99
                },
                "epsilon": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "epsilon",
                    "default": 0.001
                },
                "center": {
                    "type": "boolean",
                    "title": "Center",
                    "default": True
                },
                "scale": {
                    "type": "boolean",
                    "title": "Scale",
                    "default": True
                },
                # "beta_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "gamma_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "moving_mean_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "moving_variance_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "beta_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS
                # },
                # "gamma_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS
                # },
                # "beta_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
                # "gamma_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
            },
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
