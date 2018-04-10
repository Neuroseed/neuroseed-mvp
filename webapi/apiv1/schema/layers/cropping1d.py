import metadata

CROPPING1D_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Cropping1D$"
        },
        "config": {
            "type": "object",
            "properties": {
                "cropping": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 2,
                    "items": {
                        "type": "integer"
                    }
                },
            },
            "required": ["cropping"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
