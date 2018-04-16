ENUM_OPTIMIZER_NAME = [
    "SGD",
    "RMSprop",
    "Adagrad",
    "Adadelta",
    "Adam",
    "Adamax",
    "Nadam"
]

ENUM_LOSS = [
    "mean_squared_error",
    "mean_absolute_error",
    "mean_absolute_percentage_error",
    "mean_squared_logarithmic_error",
    "squared_hinge",
    "hinge",
    "categorical_hinge",
    "logcosh",
    "categorical_crossentropy",
    "sparse_categorical_crossentropy",
    "binary_crossentropy",
    "kullback_leibler_divergence",
    "poisson",
    "cosine_proximity"
]

ENUM_METRICS = [
    "binary_accuracy",
    "categorical_accuracy",
    "sparse_categorical_accuracy",
    "top_k_categorical_accuracy",
    "sparse_top_k_categorical_accuracy"
]

MODEL_TRAIN_SCHEMA = {
    "type": "object",
    "title": "Train model",
    "description": "Train model task",
    "properties": {
        "epochs": {
            "type": "integer",
            "minimal": 1,
            "maximal": 10000,
            "title": "Epochs",
            "description": "Number of epochs to train the model. An epoch is an iteration over the entire dataset.",
            "default": 1
        },
        "optimizer": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "enum": ENUM_OPTIMIZER_NAME,
                    "title": "Optimizer",
                    "description": "Optimizer name",
                    "default": "SGD"
                },
                "config": {
                    "type": "object",
                    "title": "Config",
                    "description": "Optimizer config",
                    "default": {}
                }
            },
            "title": "Optimizer",
            "description": "Optimizer name",
            "default": {"name": "SGD"},
            "required": ["name"],
            "additionalProperties": False
        },
        "loss": {
            "type": "string",
            "enum": ENUM_LOSS,
            "title": "Loss function",
            "description": "Name of loss function",
            "default": "mean_squared_error"
        },
        "metrics": {
            "type": "array",
            "minItems": 0,
            "maxItems": len(ENUM_METRICS),
            "items": {
                "type": "string",
                "enum": ENUM_METRICS
            },
            "title": "Metrics",
            "description": "Metrics array",
            "default": [],
            "uniqueItems": True
        }
    },
    "required": ["optimizer", "loss"],
    "additionalProperties": False
}
