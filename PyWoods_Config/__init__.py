import os
BASE_PATH: str = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR: str = os.path.join(BASE_PATH, "models")
JSON_DIR: str = os.path.join(BASE_PATH, "json_configs")

__all__ = [
    'MODELS_DIR',
    'JSON_DIR'
]