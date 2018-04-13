import metadata

TASK_SCHEMA = {
    "type": "object",
    "title": "Task",
    "description": "Task metadata",
    "properties": {
        "command": {
            "type": "string",
            "enum": metadata.task.TASK_COMMANDS,
            "title": "Command",
            "description": "Task command",
        },
        "config": {
            "type": "object",
            "title": "Task config",
            "description": "Task config",
            "default": {}
        }
    },
    "required": ["command"],
    "additionalProperties": False
}
