from .constants import *

AVERAGEPOOLING2D_LAY = {
    "type": "object",
    "title": "AveragePooling2D",
    "description": "Average pooling operation for spatial data",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^AveragePooling2D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "AveragePooling2D"
        },
        "config": {
            "type": "object",
            "properties": {
                "pool_size": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 2*10,
                    },
                    "title": "Pool size",
                    "default": [2, 2]
                },
                "strides": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 2*10
                    },
                    "title": "Strides",
                    "default": None
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING,
                    "title": "Padding",
                    "default": "valid"
                }
            },
            "required": ["pool_size"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
