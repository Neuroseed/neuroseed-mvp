import metadata

GAUSSIANNOISE_LAY = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^GaussianNoise$"
        },
        "config": {
            "type": "object",
            "properties": {
                "stddev": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                },
            },
            "required": ["stddev"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
