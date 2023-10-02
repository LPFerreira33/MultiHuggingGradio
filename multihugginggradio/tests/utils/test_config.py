import os
import pathlib
import pytest

from multihugginggradio.utils.config.config import Config, UIConfig


class TestConfig:
    """
    A test class for verifying configuration file functionality.

    This class contains three test methods, one for checking the presence of keys in a configuration file with resources,
    other for checking the presence of keys in a configuration file without resources, and another to check if
    FileNotFoundError is raised if file does not exist.
    """

    def test_path_with_resources(self):
        """
        Test the presence of specific keys in a configuration file with resources.

        This method checks if the 'AVAILABLE_MODELS', 'REPRODUCIBILITY', and 'VERBOSE' keys are present in the
        configuration file loaded using the `UIConfig.get_config` method.
        """
        config = UIConfig.get_config('config.yaml')

        assert 'AVAILABLE_MODELS' in config, 'Failed! AVAILABLE_MODELS key was not found in config!'
        assert 'REPRODUCIBILITY' in config, 'Failed! REPRODUCIBILITY key was not found in config!'
        assert 'VERBOSE' in config, 'Failed! VERBOSE key was not found in config!'

    def test_path_without_resources(self):
        """
        Test the presence of specific keys in a configuration file without resources.

        This method constructs the path to a mock configuration file and checks if the 'AVAILABLE_MODELS',
        'REPRODUCIBILITY', and 'VERBOSE' keys are present in the configuration file loaded using the `Config.get_config`
        method.
        """
        path_to_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'resources', 'mock_config.yaml')
        config = Config.get_config(path_to_file)

        assert 'AVAILABLE_MODELS' in config, 'Failed! AVAILABLE_MODELS key was not found in config!'
        assert 'REPRODUCIBILITY' in config, 'Failed! REPRODUCIBILITY key was not found in config!'
        assert 'VERBOSE' in config, 'Failed! VERBOSE key was not found in config!'

    def test_path_to_file_not_found(self):
        """
        Test for handling the case where the configuration file is not found.

        This method attempts to load a configuration file that does not exist ('not_a_file.yaml') using the
        Config.get_config` method. It expects a `FileNotFoundError` to be raised as a result.
        """
        with pytest.raises(FileNotFoundError):
            Config.get_config('not_a_file.yaml')
