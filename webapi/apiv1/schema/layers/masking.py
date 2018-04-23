import metadata
from .constants import *

MASKING_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Masking$"
        },
        "config": {
            "type": "object",
            "properties": {
                "mask_value": {
                    "type": "number"
                },
            },
            "required": ["mask_value"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
