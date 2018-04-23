import metadata

REPEATVECTOR_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^RepeatVector$"
        },
        "config": {
            "type": "object",
            "properties": {
                "n": {
                    "minimum": 2,
                    "maximum": 6,
                    "type": "integer"
                }
            },
            "required": ["n"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
