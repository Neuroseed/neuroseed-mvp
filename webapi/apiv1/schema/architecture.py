from metadata.dataset import DATASET_CATEGORIES
from .layers import LAYERS

ARCHITECTURE_SCHEMA = {
    "type": "object",
    "title": "Architecture",
    "description": "Architecture metadata",
    "properties": {
        "is_public": {
            "type": "boolean",
            "title": "Is public",
            "description": "Is architecture public",
            "default": False
        },
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "title": "Architecture title",
            "description": "Architecture title",
            "default": ""
        },
        "description": {
            "type": "string",
            "maxLength": 128,
            "title": "Architecture description",
            "description": "Architecture description",
            "default": ""
        },
        "category": {
            "type": "string",
            "enum": DATASET_CATEGORIES,
            "title": "Category",
            "description": "Architecture category",
            "default": DATASET_CATEGORIES[0]
        },
        "architecture": {
            "type": "object",
            "properties": {
                "layers": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 100,
                    "items": {
                        "oneOf": LAYERS
                    },
                    "title": "Architecture layers",
                    "description": "Architecture layers",
                    "default": None
                }
            },
            "title": "Architecture",
            "description": "Model architecture",
            "default": None,
            "required": ["layers"],
            "additionalProperties": False
        }
    },
    "required": ["title", "architecture"],
    "additionalProperties": False
}
