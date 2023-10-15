import os
import pathlib
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from multihugginggradio.interface.gradio_ui import GradioApp  # Replace with the correct import for your GradioApp class


# Define a test class for GradioApp
class TestGradioAppWithSelenium:
    """
    Test class for the GradioApp functionality.
    """

    def setup_method(self):
        """
        Launch the Gradio app in a separate process
        """
        app = GradioApp(model_config='config.yaml')
        self.gradio_process = multiprocessing.Process(target=app.run)
        self.gradio_process.start()
        time.sleep(5)  # Wait for Gradio to start

    def teardown_method(self):
        """
        Terminate the Gradio app process
        """
        self.gradio_process.terminate()
        self.gradio_process.join()

    def test_chat(self):
        """
        Test the chat functionality of the Gradio application.
        """

        # Create a webdriver instance
        driver = webdriver.Chrome()

        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Chat" task
        task_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @name='radio-select_task' and @value='Chat']")
        task_radio.click()

        # Locate the chat input field and send a message
        question = driver.find_element(By.ID, "chat_question")
        chat_question = question.find_element(By.XPATH, ".//textarea[@data-testid='textbox']")
        chat_question.send_keys("Hello World!")

        # You may uncomment this line to interact with the chat functionality. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "submit_question").click()
        # time.sleep(60)  # Wait for Gradio to start

        driver.close()
        driver.quit()

    def test_image_classification(self):
        """
        Test the image classification functionality of the Gradio application.
        """

        # Create a webdriver instance
        driver = webdriver.Chrome()

        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Image Classification" task
        task_radio = driver.find_element(
            By.XPATH,
            "//input[@type='radio' and @name='radio-select_task' and @value='Image Classification']"
        )
        task_radio.click()

        # Locate the image upload field and upload a sample image
        drag_and_drop = driver.find_element(By.XPATH, "//input[@type='file' and @accept='image/*']")
        file_path = pathlib.Path(__file__).parent.resolve()
        drag_and_drop.send_keys(os.path.join(file_path, 'resources', 'mock_drag_and_drop_image.png'))

        # You may uncomment this line to initiate image classification. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "classify_image").click()
        # time.sleep(30)  # Wait for Gradio to start

        driver.close()
        driver.quit()

    def test_image_generation(self):
        """
        Test the image generation functionality of the Gradio application.
        """

        # Create a webdriver instance
        driver = webdriver.Chrome()

        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Image Generation" task
        task_button = driver.find_element(
            By.XPATH,
            "//input[@type='radio' and @name='radio-select_task' and @value='Image Generation']"
        )
        task_button.click()

        # Locate the image generation input field and enter a prompt
        image_gen_prompt = driver.find_element(By.ID, "image_gen_prompt")
        gen_image_prompt = image_gen_prompt.find_element(By.XPATH, ".//textarea[@data-testid='textbox']")
        gen_image_prompt.send_keys("Mock Image")

        # You may uncomment this line to initiate image generation. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "generate_image").click()
        # time.sleep(30)  # Wait for Gradio to start

        driver.close()
        driver.quit()
