import metadata

GAUSSIANDROPOUT_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^GaussianDropout$"
        },
        "config": {
            "type": "object",
            "properties": {
                "rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
            },
            "required": ["rate"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
