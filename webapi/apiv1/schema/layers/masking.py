import metadata
from .constants import *

MASKING_LAY = {
    "type": "object",
    "title": "Masking",
    "description": "Masks a sequence by using a mask value to skip timesteps",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Masking$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Masking"
        },
        "config": {
            "type": "object",
            "properties": {
                "mask_value": {
                    "type": "number",
                    "title": "Mask value",
                    "description": "",
                    "default": 0
                },
            },
            "required": ["mask_value"],
            "additionalProperties": False
        }
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
