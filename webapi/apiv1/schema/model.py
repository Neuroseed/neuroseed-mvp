MODEL_SCHEMA = {
    "type": "object",
    "title": "Model",
    "description": "Model metadata",
    "properties": {
        "is_public": {
            "type": "boolean",
            "title": "Is public",
            "description": "Is architecture public",
            "default": False
        },
        "title": {
            "type": "string",
            "minLength": 3,
            "maxLength": 128,
            "title": "Architecture title",
            "description": "Architecture title",
            "default": ""
        },
        "description": {
            "type": "string",
            "maxLength": 4096,
            "title": "Model description",
            "description": "Model description",
            "default": ""
        },
        "labels": {
            "type": "array",
            "minItems": 0,
            "maxItems": 10000,
            "items": {
                "type": "string",
                "maxLength": 64
            },
            "title": "Labels",
            "description": "Model labels",
            "default": [],
            "uniqueItems": True
        },
        "architecture": {
            "type": "string",
            "maxLength": 128,
            "title": "Architecture",
            "description": "Architecture ID"
        },
        "dataset": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "title": "Dataset",
            "description": "Dataset ID"
        }
    },
    "required": ["title", "architecture", "dataset"],
    "additionalProperties": False
}
