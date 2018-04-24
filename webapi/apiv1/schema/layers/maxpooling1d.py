import metadata
from .constants import *

MAXPOOLING1D_LAY = {
    "type": "object",
    "title": "MaxPooling1D",
    "description": "Max pooling operation for temporal data",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^MaxPooling1D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "MaxPooling1D"
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
                    "minItems": 1,
                    "maxItems": 1000,
                    "title": "Strides",
                    "default": 1
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
