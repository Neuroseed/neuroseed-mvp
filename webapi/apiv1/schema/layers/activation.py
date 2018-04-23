from .constants import ACTIVATIONS_NO_LINEAR


ACTIVATION_LAY = {
    "type": "object",
    "title": "Activation",
    "description": "Applies an activation function to an output",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^Activation$",
            "title": "Layer name",
            "description": "Name of layer",
            "default": "Activation"
        },
        "config": {
            "type": "object",
            "properties": {
                "activation": {
                    "type": "string",
                    "enum": ACTIVATIONS_NO_LINEAR,
                    "title": "Activation",
                    "description": "Activation type",
                    "default": ACTIVATIONS_NO_LINEAR[0]
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["name"],
    "additionalProperties": False
}
