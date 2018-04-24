import metadata

ACTIVITYREGULARIZATION_LAY = {
    "type": "object",
    "title": "ActivityRegularization",
    "description": "Layer that applies an update to the cost function based input activity",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^ActivityRegularization$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "ActivityRegularization"
        },
        "config": {
            "type": "object",
            "properties": {
                "l1": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000,
                    "title": "L2",
                    "default": 0
                },
                "l2": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000,
                    "title": "L2",
                    "default": 0
                },
                # "input_shape": {
                #     "type": "array",
                #     "minItems": 2,
                #     "maxItems": 6,
                #     "items": {
                #         "type": "integer"
                #     },
                # },
            },
            "required": ["l1", "l2"],
            "additionalProperties": False
        },
    },
    "required": ["name", "config"],
    "additionalProperties": False
}
