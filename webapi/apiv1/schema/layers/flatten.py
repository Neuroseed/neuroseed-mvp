import metadata

FLATTEN_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Flatten$"
        },
        "config": {
            "type": "object",
            "properties": {},
        },
        "additionalProperties": False
    },
    "required": ["name"],
    "additionalProperties": False
}
