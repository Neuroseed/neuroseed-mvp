MODEL_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "title": "Dataset",
            "description": "Dataset ID"
        }
    }
}
