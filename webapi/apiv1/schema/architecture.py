ARCHITECTURE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "is_public": {"type": "boolean"},
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 128
        },
        "category": {
            "type": "string",
            "maxLength": 128
        },
        "architecture": {
            "type": "object",
            "properties": {
                "layers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "config": {"type": "object"}
                        },
                        "required": ["name"],
                        "additionalProperties": False
                    },
                }
            },
            "required": ["layers"],
            "additionalProperties": False
        }
    },
    "required": ["title", "architecture"],
    "additionalProperties": False
}