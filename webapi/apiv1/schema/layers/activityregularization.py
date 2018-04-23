import metadata

ACTIVITYREGULARIZATION_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^ActivityRegularization$"
        },
        "config": {
            "type": "object",
            "properties": {
                "l1": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000,
                },
                "l2": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000,
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
            "required": ["l1", "l2"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
