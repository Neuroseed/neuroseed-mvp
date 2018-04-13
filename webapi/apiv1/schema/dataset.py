import metadata

DATASET_SCHEMA = {
    "type": "object",
    "title": "Dataset",
    "description": "Dataset metadata",
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
            "title": "Dataset title",
            "description": "Dataset title",
            "default": ""
        },
        "description": {
            "type": "string",
            "maxLength": 4096,
            "title": "Dataset description",
            "description": "Dataset description",
            "default": ""
        },
        "category": {
            "type": "string",
            "enum": metadata.dataset.DATASET_CATEGORIES,
            "title": "Category",
            "description": "Dataset category",
            "default": metadata.dataset.DATASET_CATEGORIES[0]
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
            "description": "Dataset labels",
            "default": [],
            "uniqueItems": True
        }
    },
    "required": ["title"],
    "additionalProperties": False
}
