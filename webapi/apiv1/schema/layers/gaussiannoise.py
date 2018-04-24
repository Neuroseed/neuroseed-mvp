import metadata

GAUSSIANNOISE_LAY = {
    "type": "object",
    "title": "GaussianNoise",
    "description": "Apply additive zero-centered Gaussian noise",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^GaussianNoise$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "GaussianNoise"
        },
        "config": {
            "type": "object",
            "properties": {
                "stddev": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "title": "Standard deviation",
                    "description": "Standard deviation of the noise distribution"
                },
            },
            "required": ["stddev"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
