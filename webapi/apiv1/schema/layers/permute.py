import metadata

PERMUTE_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Permute$"
        },
        "config": {
            "type": "object",
            "properties": {
                "dims": {
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
            "required": ["dims"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
