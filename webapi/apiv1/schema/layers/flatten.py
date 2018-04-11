
FLATTEN_LAY = {
    "type": "object",
    "title": "Flatten",
    "description": "Flattens the input",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Flatten$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Flatten"
        },
        "config": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    "required": ["name"],
    "additionalProperties": False
}
