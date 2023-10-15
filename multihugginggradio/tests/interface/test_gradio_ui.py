import pytest
import time
import threading
from multihugginggradio.interface.gradio_ui import GradioApp  # Replace with the correct import for your GradioApp class


# Define a fixture to set up and tear down the GradioApp for testing
@pytest.fixture
def gradio_app():
    """
    Fixture to initialize a GradioApp instance, start its interface in a background thread, and clean up after the test.
    """
    # Initialize the GradioApp with a model configuration file 'config.yaml'
    app = GradioApp(model_config='config.yaml')

    # Create a thread to run the Gradio interface in the background
    thread = threading.Thread(target=app.run)
    thread.daemon = True
    thread.start()

    # Give some time for the Gradio interface to start (adjust as needed)
    time.sleep(5)

    # Yield the GradioApp instance for the test
    yield app

    # Terminate the Gradio interface after the test
    app.demo.close()
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
    def test_running_interface(self, gradio_app):
        """
        Test various attributes and methods related to the running Gradio interface.
        """
        assert hasattr(gradio_app, 'demo'), "GradioApp does not have 'demo' attribute."
        assert hasattr(gradio_app, 'question'), "GradioApp does not have 'question' attribute."
        assert hasattr(gradio_app, 'upload_image'), "GradioApp does not have 'upload_image' attribute."
        assert hasattr(gradio_app, 'select_chat_model'), "GradioApp does not have 'select_chat_model' attribute."
        assert hasattr(gradio_app, 'select_image_class_model'), "GradioApp does not have 'select_image_class_model' attribute."
        assert hasattr(gradio_app, 'answer'), "GradioApp does not have 'answer' attribute."
        assert hasattr(gradio_app, 'elapsed_time'), "GradioApp does not have 'elapsed_time' attribute."
        assert hasattr(gradio_app, 'submit_question'), "GradioApp does not have 'submit_question' attribute."
        assert hasattr(gradio_app, 'submit_image'), "GradioApp does not have 'submit_image' attribute."
        assert hasattr(gradio_app, 'interface_objects'), "GradioApp does not have 'interface_objects' attribute."
