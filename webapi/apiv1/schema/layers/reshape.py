import metadata

RESHAPE_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Reshape$"
        },
        "config": {
            "type": "object",
            "properties": {
                "target_shape": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 6,
                    "items": {
                        "type": "integer"
                    }
                },
                "input_shape": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 6,
                    "items": {
                        "type": "integer"
                    },
                },
            },
            "required": ["target_shape"],
            "additionalProperties": False,
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
