import metadata
from .constants import *

AVERAGEPOOLING1D_LAY = {
    "type": "object",
    "title": "AveragePooling1D",
    "description": "Average pooling for temporal data",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^AveragePooling1D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "AveragePooling1D"
        },
        "config": {
            "type": "object",
            "properties": {
                "pool_size": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 1000,
                    "title": "Pool size",
                    "default": 2
                },
                "strides": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                    "title": "Strides",
                    "default": None
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING,
                    "title": "Padding",
                    "default": "valid"
                },
            },
            "required": ["pool_size"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
