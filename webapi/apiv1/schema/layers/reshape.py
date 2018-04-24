import metadata

RESHAPE_LAY = {
    "type": "object",
    "title": "Reshape",
    "description": "Reshapes an output to a certain shape",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Reshape$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Reshape"
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
                    },
                    "title": "Target shape",
                    "description": "Target shape. Tuple of integers. Does not include the batch axis."
                },
                # "input_shape": {
                #     "type": "array",
                #     "minItems": 2,
                #     "maxItems": 6,
                #     "items": {
                #         "type": "integer"
                #     },
                # },
            },
            "required": ["target_shape"],
            "additionalProperties": False,
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
