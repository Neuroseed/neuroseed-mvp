import metadata

CROPPING1D_LAY = {
    "type": "object",
    "title": "Cropping1D",
    "description": "Cropping layer for 1D input",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Cropping1D$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Cropping1D"
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
                    },
                    "title": "Cropping",
                    "description": "How many units should be trimmed off at the beginning and end of the cropping dimension (axis 1)"
                },
            },
            "required": ["cropping"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
