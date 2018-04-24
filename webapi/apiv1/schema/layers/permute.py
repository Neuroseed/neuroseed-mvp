import metadata

PERMUTE_LAY = {
    "type": "object",
    "title": "Permute",
    "description": "Permutes the dimensions of the input according to a given pattern",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Permute$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Permute"
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
                    },
                    "title": "Dims",
                    "description": "Tuple of integers. Permutation pattern, does not include the samples dimension.",
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
            "required": ["dims"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
