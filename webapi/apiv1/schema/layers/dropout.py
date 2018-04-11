
DROPOUT_LAY = {
    "type": "object",
    "title": "Dropout",
    "description": "Apply Dropout to the input",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Dropout$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Dropout"
        },
        "config": {
            "type": "object",
            "properties": {
                "rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Rate",
                    "default": 0.25
                },
                "noise_shape": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 5,
                    "items": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 2*20,
                    },
                    "title": "Noise shape",
                    "default": None
                },
                "seed": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 2*10,
                    "title": "Seed",
                    "default": None
                },
            },
            "required": ["rate"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
