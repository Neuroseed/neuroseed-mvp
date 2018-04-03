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
    "properties": {
        "epochs": {"type": "number"},
        "optimizer": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "enum": ENUM_OPTIMIZER_NAME
                },
                "config": {"type": "object"}
            },
            "required": ["name"],
            "additionalProperties": False
        },
        "loss": {
            "type": "string",
            "enum": ENUM_LOSS
        },
        "metrics": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ENUM_METRICS
            },
            "uniqueItems": True
        }
    },
    "required": ["optimizer", "loss"],
    "additionalProperties": False
}
