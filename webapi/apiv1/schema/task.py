import metadata

TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "enum": metadata.task.TASK_COMMANDS
        },
        "config": {"type": "object"}
    },
    "required": ["command"],
    "additionalProperties": False
}
