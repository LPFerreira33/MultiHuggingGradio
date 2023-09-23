import os
import yaml
from importlib.resources import is_resource, open_binary


class Config(object):
    @staticmethod
    def get_config(config_file: str, resources_location: str = None) -> dict:
        """
        Retrieve configuration data from a YAML file.

        Parameters:
            config_file (str): The path to the YAML configuration file.
            resources_location (str, optional): The location of the resources. If specified, it looks
                                                for the configuration file within the specified resources.
                                                Defaults to None.

        Returns:
            dict: A dictionary containing the configuration data.

        This method reads the specified YAML configuration file either from the local filesystem
        or from resources. If a `resources_location` is provided and the file exists within those
        resources, it reads the data from the resource. Otherwise, if the file exists in the local
        filesystem, it reads the data from there. The configuration data is returned as a dictionary.
        """

        if resources_location is not None and is_resource(resources_location, config_file):
            with open_binary(resources_location, config_file) as f:
                data = yaml.safe_load(f)
        elif os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                data = yaml.safe_load(f)
        else:
            raise FileNotFoundError

        return data


class UIConfig(Config):
    RESOURCE_LOCATION = 'multihugginggradio.resources'

    @staticmethod
    def get_config(config_file: str) -> dict:
        """
        Retrieve configuration data specifically for the UI.

        Parameters:
            config_file (str): The path to the YAML configuration file.

        Returns:
            dict: A dictionary containing the UI-specific configuration data.

        This method is a specialization of the base `Config.get_config` method. It calls the base method
        with the specific `RESOURCE_LOCATION` for the UI resources. The configuration data related to
        the UI is returned as a dictionary.
        """
        return super(UIConfig, UIConfig).get_config(config_file, UIConfig.RESOURCE_LOCATION)
