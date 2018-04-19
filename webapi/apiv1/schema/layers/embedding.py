import metadata
from .constants import *

EMBEDDING_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Embedding$"
        },
        "config": {
            "type": "object",
            "properties": {
                "input_dim": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100000,
                },
                "output_dim": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100000,
                },
                "embeddings_initializer": {
                    "type": "string",
                    "enum": INITIALIZERS
                },
                "embeddings_regularizer": {
                    "type": "string",
                    "enum": REGULARIZERS
                },
                "embeddings_constraint": {
                    "type": "string",
                    "enum": CONSTRAINTS
                },
                "mask_zero": {
                    "type": "boolean",
                },
            },
            "required": ["input_dim"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
