MODEL_SCHEMA = {
    "type": "object",
    "properties": {
        "is_public": {"type": "boolean"},
        "title": {
            "type": "string",
            "minLength": 3,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 64
            },
            "uniqueItems": True
        },
        "architecture": {
            "type": "string",
            "maxLength": 128
        },
        "dataset": {
            "type": "string",
            "maxLength": 128
        }
    },
    "required": ["title", "architecture", "dataset"],
    "additionalProperties": False
}
