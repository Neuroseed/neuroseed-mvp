import metadata
from .constants import *

MAXPOOLING1D_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^MaxPooling1D$"
        },
        "config": {
            "type": "object",
            "properties": {
                "pool_size": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 1000,
                },
                "strides": {
                    "type": "integer",
                    "minItems": 2,
                    "maxItems": 1000,
                },
                "padding": {
                    "type": "string",
                    "enum": PADDING
                },
            },
            "required": ["pool_size"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
