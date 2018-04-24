import metadata
from .constants import *

EMBEDDING_LAY = {
    "type": "object",
    "title": "Embedding",
    "description": "Turns positive integers (indexes) into dense vectors of fixed size",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Embedding$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Embedding"
        },
        "config": {
            "type": "object",
            "properties": {
                "input_dim": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100000,
                    "title": "Input dim",
                    "description": "Size of the vocabulary",
                    "default": 1
                },
                "output_dim": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100000,
                    "title": "Output dim",
                    "description": "Dimension of the dense embedding",
                    "default": 1
                },
                # "embeddings_initializer": {
                #     "type": "string",
                #     "enum": INITIALIZERS
                # },
                # "embeddings_regularizer": {
                #     "type": "string",
                #     "enum": REGULARIZERS
                # },
                # "embeddings_constraint": {
                #     "type": "string",
                #     "enum": CONSTRAINTS
                # },
                # "mask_zero": {
                #     "type": "boolean",
                # },
            },
            "required": ["input_dim"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
