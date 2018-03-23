TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "command": {"type": "string"},
        "config": {"type": "object"}
    },
    "additionalProperties": False
}

MODEL_TRAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset": {"type": "string"},
        "epochs": {"type": "number"}
    },
    "additionalProperties": False
}
