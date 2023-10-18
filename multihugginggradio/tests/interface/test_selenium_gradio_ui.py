import os
import pathlib
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.app = GradioApp(model_config='config.yaml')

        self.gradio_process = multiprocessing.Process(target=self.app.run)
        self.gradio_process.daemon = False
        self.gradio_process.start()
        time.sleep(10)  # Wait for Gradio to start

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
        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--ignore-certificate-errors",
        ]
        for option in options:
            chrome_options.add_argument(option)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Create a webdriver instance
        driver = webdriver.Chrome(options=chrome_options)

        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Chat" task
        chat_xpath = "//input[@type='radio' and @name='radio-select_task' and @value='Chat']"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, chat_xpath)))
        task_radio = driver.find_element(By.XPATH, chat_xpath)
        task_radio.click()

        # Locate the chat input field and send a message
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "chat_question")))
        question = driver.find_element(By.ID, "chat_question")
        chat_question = question.find_element(By.XPATH, ".//textarea[@data-testid='textbox']")
        chat_question.send_keys("Hello World!")
        driver.implicitly_wait(1)

        # You may uncomment this line to interact with the chat functionality. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "submit_question").click()
        # driver.implicitly_wait(60)

        driver.close()
        driver.quit()

    def test_image_classification(self):
        """
        Test the image classification functionality of the Gradio application.
        """

        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--ignore-certificate-errors",
        ]
        for option in options:
            chrome_options.add_argument(option)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Create a webdriver instance
        driver = webdriver.Chrome(options=chrome_options)

        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Image Classification" task
        image_class_xpath = "//input[@type='radio' and @name='radio-select_task' and @value='Image Classification']"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, image_class_xpath)))
        task_radio = driver.find_element(By.XPATH, image_class_xpath)
        task_radio.click()

        # Locate the image upload field and upload a sample image
        drag_and_drop_xpath = "//input[@type='file' and @accept='image/*']"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, drag_and_drop_xpath)))
        drag_and_drop = driver.find_element(By.XPATH, drag_and_drop_xpath)
        file_path = pathlib.Path(__file__).parent.resolve()
        drag_and_drop.send_keys(os.path.join(file_path, 'resources', 'mock_drag_and_drop_image.png'))
        driver.implicitly_wait(1)

        # You may uncomment this line to initiate image classification. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "classify_image").click()
        # driver.implicitly_wait(30)

        driver.close()
        driver.quit()

    def test_image_generation(self):
        """
        Test the image generation functionality of the Gradio application.
        """
        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--ignore-certificate-errors",
        ]
        for option in options:
            chrome_options.add_argument(option)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Create a webdriver instance
        driver = webdriver.Chrome(options=chrome_options)
        # Open your Gradio application in a new browser window
        driver.get("http://127.0.0.1:7860")

        # Select the "Image Generation" task
        image_gen_xpath = "//input[@type='radio' and @name='radio-select_task' and @value='Image Generation']"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, image_gen_xpath)))
        task_button = driver.find_element(By.XPATH, image_gen_xpath)
        task_button.click()

        # Locate the image generation input field and enter a prompt
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "image_gen_prompt")))
        image_gen_prompt = driver.find_element(By.ID, "image_gen_prompt")
        gen_image_prompt = image_gen_prompt.find_element(By.XPATH, ".//textarea[@data-testid='textbox']")
        gen_image_prompt.send_keys("Mock Image")
        driver.implicitly_wait(1)

        # You may uncomment this line to initiate image generation. Increases coverage, but may lead to crashes.
        # driver.find_element(By.ID, "generate_image").click()
        # driver.implicitly_wait(60)

        driver.close()
        driver.quit()
