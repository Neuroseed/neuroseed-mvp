import metadata

REPEATVECTOR_LAY = {
    "type": "object",
    "title": "RepeatVector",
    "description": "Repeats the input n times",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^RepeatVector$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "RepeatVector"
        },
        "config": {
            "type": "object",
            "properties": {
                "n": {
                    "minimum": 2,
                    "maximum": 6,
                    "type": "integer",
                    "title": "n",
                    "description": "Integer, repetition factor"
                }
            },
            "required": ["n"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
