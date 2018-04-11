from .layers import LAYERS

ARCHITECTURE_SCHEMA = {
    "type": "object",
    "properties": {
        "is_public": {"type": "boolean"},
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 128
        },
        "category": {
            "type": "string",
            "maxLength": 128
        },
        "architecture": {
            "type": "object",
            "properties": {
                "layers": {
                    "type": "array",
                    "items": {
                        "oneOf": LAYERS
                    },
                }
            },
            "required": ["layers"],
            "additionalProperties": False
        }
    },
    "required": ["title", "architecture"],
    "additionalProperties": False
}
