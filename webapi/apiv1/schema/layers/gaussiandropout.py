import metadata

GAUSSIANDROPOUT_LAY = {
    "type": "object",
    "title": "GaussianDropout",
    "description": "Apply multiplicative 1-centered Gaussian noise",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^GaussianDropout$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "GaussianDropout"
        },
        "config": {
            "type": "object",
            "properties": {
                "rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Rate",
                    "default": 0.25
                },
            },
            "required": ["rate"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
