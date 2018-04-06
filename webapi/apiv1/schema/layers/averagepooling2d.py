import metadata
from .constants import *

AVERAGEPOOLING2D_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^AveragePooling2D$"
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
                    },
                },
                "strides":{
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "integer",
                    },
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING
                },
                "data_format": {
                    "minLength": 6,
                    "maxLength": 16,
                    "type": "string",
                },
            },
            "required": ["pool_size"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
