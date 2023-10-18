import pytest
import os
import time
import threading
import pathlib
from PIL import Image

from multihugginggradio.interface.gradio_ui import GradioApp  # Replace with the correct import for your GradioApp class


# Define a fixture to set up and tear down the GradioApp for testing
@pytest.fixture
def gradio_app():
    """
    Fixture to initialize a GradioApp instance.
    """
    # Initialize the GradioApp with a model configuration file 'config.yaml'
    app = GradioApp(model_config='config.yaml')

    # Yield the GradioApp instance for the test
    yield app


# Define a fixture to set up and tear down the threaded GradioApp for testing
@pytest.fixture
def run_gradio_app(gradio_app):
    """
    Fixture to initialize a GradioApp instance, start its interface in a background thread, and clean up after the test.
    """
    # Create a thread to run the Gradio interface in the background
    thread = threading.Thread(target=gradio_app.run, daemon=False)
    thread.start()

    # Give some time for the Gradio interface to start
    time.sleep(5)

    # Yield the GradioApp instance for the test
    yield gradio_app

    gradio_app.demo.close()
    thread.join()


# Define a test class for GradioApp
class TestGradioApp:
    """
    Test class for the GradioApp functionality.
    """
    # Test the initialization of GradioApp
    def test_init(self, gradio_app):
        """
        Test GradioApp initialization and check for the existence of various attributes.
        """
        assert isinstance(gradio_app, GradioApp), "GradioApp is not an instance of GradioApp class."

        # Check for the existence of various attributes in GradioApp
        assert hasattr(gradio_app, 'config'), "GradioApp does not have 'config' attribute."
        assert hasattr(gradio_app, 'available_models'), "GradioApp does not have 'available_models' attribute."
        assert hasattr(gradio_app, 'seed'), "GradioApp does not have 'seed' attribute."
        assert hasattr(gradio_app, 'verbose'), "GradioApp does not have 'verbose' attribute."
        assert hasattr(gradio_app, 'models'), "GradioApp does not have 'models' attribute."
        assert hasattr(gradio_app, 'timers'), "GradioApp does not have 'timers' attribute."

    # Test the available models dictionary in GradioApp
    def test_available_models(self, gradio_app):
        """
        Test the 'available_models' dictionary in GradioApp.
        """
        assert isinstance(gradio_app.available_models, dict), "available_models is not a dictionary."
        assert 'Chat' in gradio_app.available_models, "Chat model is not available."
        assert 'Image Classification' in gradio_app.available_models, "Image Classification model is not available."
        assert 'Image Generation' in gradio_app.available_models, "Image Generation model is not available."

    # Test various attributes and methods related to the running interface
    def test_running_interface(self, run_gradio_app):
        """
        Test various attributes and methods related to the running Gradio interface.
        """
        assert hasattr(run_gradio_app, 'demo'), "GradioApp does not have 'demo' attribute."
        assert hasattr(run_gradio_app, 'question'), "GradioApp does not have 'question' attribute."
        assert hasattr(run_gradio_app, 'upload_image'), "GradioApp does not have 'upload_image' attribute."
        assert hasattr(run_gradio_app, 'select_chat_model'), "GradioApp does not have 'select_chat_model' attribute."
        assert hasattr(run_gradio_app, 'select_image_class_model'), \
            "GradioApp does not have 'select_image_class_model' attribute."
        assert hasattr(run_gradio_app, 'answer'), "GradioApp does not have 'answer' attribute."
        assert hasattr(run_gradio_app, 'elapsed_time'), "GradioApp does not have 'elapsed_time' attribute."
        assert hasattr(run_gradio_app, 'submit_question'), "GradioApp does not have 'submit_question' attribute."
        assert hasattr(run_gradio_app, 'submit_image'), "GradioApp does not have 'submit_image' attribute."
        assert hasattr(run_gradio_app, 'interface_objects'), "GradioApp does not have 'interface_objects' attribute."

    def test_change_interface(self, run_gradio_app):
        objects_list = run_gradio_app.change_interface('Chat')
        assert isinstance(objects_list, list), "Change Interface does not return a list"

    def test_chat(self, gradio_app):
        result, elapsed_time_text = gradio_app.ask_chat_model("Hello", 'databricks/dolly-v2-3b')
        assert isinstance(result, str), "Result is not the correct type"
        assert isinstance(elapsed_time_text, str), "Elapsed time is not the correct type"

        # Clear memory to avoid crashes
        gradio_app.release_models()
        assert gradio_app.models == {}, 'Models were not released correctly'

    def test_image_classification(self, gradio_app):
        file_path = pathlib.Path(__file__).parent.resolve()
        image = Image.open(os.path.join(file_path, 'resources', 'mock_drag_and_drop_image.png'))
        result, elapsed_time_text = gradio_app.classify_image_model(image, 'google/vit-base-patch16-224')
        assert isinstance(result, str), "Result is not the correct type"
        assert isinstance(elapsed_time_text, str), "Elapsed time is not the correct type"

        # Clear memory to avoid crashes
        gradio_app.release_models()
        assert gradio_app.models == {}, 'Models were not released correctly'

    def test_image_generation(self, gradio_app):
        result, elapsed_time_text = gradio_app.gen_image_model("Mock image", 'CompVis/stable-diffusion-v1-4')

        assert isinstance(result, Image.Image), "Result is not the correct type"
        assert isinstance(elapsed_time_text, str), "Elapsed time is not the correct type"

        # Clear memory to avoid crashes
        gradio_app.release_models()
        assert gradio_app.models == {}, 'Models were not released correctly'
