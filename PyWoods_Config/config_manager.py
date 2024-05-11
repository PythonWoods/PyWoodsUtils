import os
import json
import logging
from typing import Dict, Optional, Union, Type
from importlib import import_module
from pydantic import BaseModel
from gettext import gettext as _

from . import MODELS_DIR, JSON_DIR

class ConfigManager:
    """
    Classe per la gestione delle configurazioni dei modelli.
    """

    class Config(BaseModel):
        pass

    _model_to_json_map: Dict[str, str] = {}
    _json_data_cache: Dict[str, str] = {}  # Cache for JSON data

    @classmethod
    def json_dir(cls) -> str:
        """
        Returns the directory containing JSON configuration files.
        """
        return JSON_DIR

    @classmethod
    def models_dir(cls) -> str:
        """
        Returns the directory containing model configuration files.
        """
        return MODELS_DIR

    @classmethod
    def _find_model_json_files(cls) -> Dict[str, str]:
        """
        Scans the models directory for configuration files and builds a map
        to their corresponding JSON files.

        Returns:
            A dictionary mapping model names to JSON file paths.
        """
        model_to_json_map: Dict[str, str] = {}

        # Get the list of files in the models directory
        file_list = os.listdir(cls.models_dir())

        # Define files to exclude
        files_to_exclude = ["__init__.py", "base_config.py"]

        # Iterate over all files in the models directory
        for file_name in file_list:
            if file_name.endswith(".py") and file_name not in files_to_exclude:
                # Remove file extension to get the base name
                base_name = os.path.splitext(file_name)[0]
                # Extract model name from the base name
                model_name = base_name.split("_")[0]
                # Build the full path to the JSON file using the model name
                json_file = os.path.join(cls.json_dir(), f"{model_name}.json")
                # Check if the JSON file exists
                if os.path.exists(json_file):
                    # If the file exists, add it to the model-JSON map
                    model_to_json_map[model_name] = json_file
                else:
                    logging.warning(_("JSON file not found for '%s': %s") % (model_name, json_file))

        return model_to_json_map

    @classmethod
    def load_configs(cls) -> Optional[Union[Type[Config], Dict[str, BaseModel]]]:
        """
        Load configurations for all models and returns:

        - An instance of Config containing configurations for all loaded models (if successful)
        - A dictionary mapping model names to their corresponding BaseModel instances (if only some models loaded successfully)
        - None if no valid model configurations found.
        """
        loaded_configs: Dict[str, BaseModel] = {}  # Dictionary to store loaded configurations
        model_to_json_map = cls._find_model_json_files()  # Find model JSON files

        # Check if the JSON data cache is empty
        if not cls._json_data_cache:
            # Fill the JSON data cache
            for model_name, json_file in model_to_json_map.items():
                try:
                    with open(json_file, 'r') as f:
                        # Read data and convert the dictionary to a JSON string before validation
                        json_data = json.load(f)
                        json_string = json.dumps(json_data)
                    cls._json_data_cache[model_name] = json_string

                except FileNotFoundError:
                    logging.error(_("JSON file not found: %s") % json_file)
                    continue
                except json.JSONDecodeError as e:
                    logging.error(_("JSON parsing error for %s: %s") % (json_file, e))
                    continue

        for model_name, json_file in model_to_json_map.items():
            try:
                # Import the corresponding model module and class
                module_name = f"{__package__}.models.{model_name}_model"
                module = import_module(module_name)
                model_class_name = f"{model_name.capitalize()}Config"

                # If the class doesn't exist in the module, log an error and continue with the next model
                if not hasattr(module, model_class_name):
                    logging.error(_("Class %s not found in module %s.") % (model_class_name, module_name))
                    continue

                # Create an instance of the model from the JSON file
                model_class = getattr(module, model_class_name)
                # Validate the JSON data against the model schema
                model_instance = model_class.model_validate_json(cls._json_data_cache[model_name])
                loaded_configs[model_name] = model_instance

                # Log successful creation of model instance
                logging.info(_("Model %s instantiated successfully from module %s.") % (model_name, module_name))

            except ImportError:
                # Log an error if the module cannot be imported
                logging.error(_("Module import error: %s") % module_name)
                continue
            except Exception as e:
                # Log any other unexpected error during model instantiation
                logging.error(_("Unexpected error during model instantiation: %s") % e)
                continue

        # Dynamically create properties in the Config class for loaded models
        for key, value in loaded_configs.items():
            setattr(cls.Config, key, value)

        # Return the Config instance if successful
        if loaded_configs:
            return cls.Config  # type: ignore
        else:
            logging.warning(_("No valid model configurations found."))
            return None
