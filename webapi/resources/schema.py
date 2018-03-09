DATASET_SCHEMA = {
    "is_public": {"type": "boolean"},
    "meta":{
        "title": {
            "type": "string",
                "minLength":1,
                "maxLength":128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "category": {
            "type": "string",
            "maxLength": 64
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength":64
            },
            "uniqueItems": True
        }
    },
    "required":["title"]
}

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
                "layers": {"type": "array"}
            }
        }
    },
    "required":["title"]
}

MODEL_SCHEMA = {
    "type": "object",
    "properties": {
        "is_public": {"type": "boolean"},
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "category": {
            "type": "string",
            "maxLength": 64
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
    "required": ["title", "architecture"]
}

TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "command": {"type": "string"},
        "config": {"type": "object"}
    }
}

MODEL_TRAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset": {"type": "string"},
        "epochs": {"type": "number"},
        "optimizer": {"type": "string"},
        "loss": {"type": "string"},
        "metrics": {
            "type": "array",
            "items": "string",
            "uniqueItems": True
        }
    },
    "additionalProperties": False,
    "required": ["dataset", "optimizer", "loss"]
}

