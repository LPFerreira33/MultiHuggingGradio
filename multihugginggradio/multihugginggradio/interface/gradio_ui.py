import time
import gradio as gr

from multihugginggradio.utils.config.config import UIConfig
from multihugginggradio.models.chat_llm import ChatLLM
from multihugginggradio.models.image_class_model import ImageClassModel
from multihugginggradio.models.image_gen_model import ImageGenModel


class GradioApp(object):
    def __init__(
        self,
        model_config: str = 'config.yaml',
    ):
        """
        Initialize a GradioApp.

        Parameters:
            model_config (str): Path to the configuration file for the GradioApp and model settings.
                               Defaults to 'config.yaml'.

        This class sets up a graphical interface using the Gradio library to interact with models
        for various tasks. It loads configuration settings from the specified
        `model_config` file, including available models and reproducibility settings.
        """
        self.config = UIConfig.get_config(model_config)
        self.available_models = self.config['AVAILABLE_MODELS']
        self.seed = self.config['REPRODUCIBILITY']['SEED']
        self.verbose = self.config['VERBOSE']

        self.models = {}
        self.timers = []

    def run(self):
        """
        Launch the Gradio interface.

        This method creates a Gradio interface allowing users to select a task (Chat or Image Classification),
        choose a model for the task, and provide input (text prompt or image). It then generates responses
        and displays the answers along with the time taken for generation.

        The interface includes the following components:
        - Radio buttons to select the task (Chat or Image Classification).
        - Textbox for entering a question (for Chat task).
        - Image upload component (for Image Classification task).
        - Dropdown menus to select a model for each task.
        - Textbox to display the generated answer.
        - Textbox to display the elapsed time for response generation.
        - Submit buttons to trigger model inference.

        """
        # Create a Gradio interface using the Blocks context
        with gr.Blocks(title="MultiHuggingGradio") as self.demo:

            # Radio buttons for selecting the task (Chat or Image Classification)
            task = gr.Radio(
                list(self.available_models.keys()),
                label="Select Task",
                elem_id="select_task",
            )

            # Create interface components for Chat task
            with gr.Row():
                with gr.Column():
                    # Textbox for user input question (Chat task)
                    self.question = gr.Textbox(label="Question", elem_id="chat_question", visible=False)
                    # Textbox for user input prompt (Image Generation task)
                    self.prompt = gr.Textbox(label="Prompt", elem_id="image_gen_prompt", visible=False)
                    # Image upload component (Image Classification task)
                    self.upload_image = gr.Image(visible=False, type="pil")

                    # Dropdown menu for selecting a chat model
                    self.select_chat_model = gr.Dropdown(
                        self.available_models['Chat'],
                        label="Models",
                        value=self.available_models['Chat'][0],
                        visible=False,
                    )

                    # Dropdown menu for selecting an image classification model
                    self.select_image_class_model = gr.Dropdown(
                        self.available_models['Image Classification'],
                        label="Models",
                        value=self.available_models['Image Classification'][0],
                        visible=False,
                    )

                    # Dropdown menu for selecting an image generation model
                    self.select_image_gen_model = gr.Dropdown(
                        self.available_models['Image Generation'],
                        label="Models",
                        value=self.available_models['Image Generation'][0],
                        visible=False,
                    )

                with gr.Column():
                    # Textbox to display the generated answer
                    self.answer = gr.Textbox(label="Answer", visible=False)

                    # Textbox to display the image classification
                    self.classification = gr.Textbox(label="Classification", visible=False)

                    # Image to display the generated image
                    self.output_image = gr.Image(label="Output Image", visible=False)

                    # Textbox to display the elapsed time for response generation
                    self.elapsed_time = gr.Textbox(label="Elapsed Time", visible=True)

            # Submit button and function for the Chat task
            self.submit_question = gr.Button("Submit Question", elem_id='submit_question', visible=False)
            self.submit_question.click(
                fn=self.ask_chat_model,
                inputs=[self.question, self.select_chat_model],
                outputs=[self.answer, self.elapsed_time],
            )

            # Submit button and function for the Image Classification task
            self.submit_image = gr.Button("Classify Image", elem_id='classify_image', visible=False)
            self.submit_image.click(
                fn=self.classify_image_model,
                inputs=[self.upload_image, self.select_image_class_model],
                outputs=[self.classification, self.elapsed_time]
            )

            # Submit button and function for the Image Generation task
            self.submit_prompt = gr.Button("Generate Image", elem_id='generate_image', visible=False)
            self.submit_prompt.click(
                fn=self.gen_image_model,
                inputs=[self.prompt, self.select_image_gen_model],
                outputs=[self.output_image, self.elapsed_time]
            )

            # Define the interface objects for each task
            self.interface_objects = {
                'Chat':
                    [self.question, self.select_chat_model, self.submit_question, self.answer],
                'Image Classification':
                    [self.upload_image, self.select_image_class_model, self.submit_image, self.classification],
                'Image Generation':
                    [self.prompt, self.select_image_gen_model, self.submit_prompt, self.output_image],
            }

            # Update interface components based on the selected task
            task.change(
                fn=self.change_interface,
                inputs=task,
                outputs=[value for values in self.interface_objects.values() for value in values],
            )

        # Launch the Gradio interface with the defined components
        self.demo.launch(share=False, server_port=7860)

    def change_interface(self, task: str):
        """
        Change the visibility of interface objects based on the selected task.

        Args:
            task (str): The task for which the interface objects should be updated.

        Returns:
            list: A list of updated interface objects.

        """
        objects_list = []

        # Iterate through the interface objects for different tasks
        for cur_task, task_objects in self.interface_objects.items():
            # Determine if the objects should be visible based on the selected task
            is_visible = task == cur_task

            # Update the visibility of each type of task object
            for task_object in task_objects:
                if str(task_object) == "textbox":
                    objects_list.append(gr.Textbox.update(visible=is_visible))
                elif str(task_object) == "button":
                    objects_list.append(gr.Button.update(visible=is_visible))
                elif str(task_object) == "dropdown":
                    objects_list.append(gr.Dropdown.update(visible=is_visible))
                elif str(task_object) == "image":
                    objects_list.append(gr.Image.update(visible=is_visible))

        return objects_list

    def classify_image_model(self, image, model_name: str):
        """
        Classify an image using a specified image classification model.

        Args:
            image: The image to be classified as a NumPy array.
            model_name (str): The name of the image classification model to use.

        Returns:
            tuple: A tuple containing the classification result and elapsed time text.

                - result: The classification result returned by the model.
                - elapsed_time_text: A string describing the time taken for the classification.

        Note:
            This method loads and initializes the specified image classification model if it
            doesn't exist in the `self.models` dictionary. It records the elapsed time for
            classification and appends it to `self.timers`.

        """
        # Record the starting time for performance measurement
        start_time = time.time()

        # Load the model if it doesn't exist yet
        if model_name not in self.models.keys():
            if self.verbose:
                print(f'Loading Model ({model_name}) for task Image Classification...')

            self.models[model_name] = ImageClassModel(model_name, self.verbose)

        # Perform inference with the specified model
        result = self.models[model_name].infer(
            image,
            seed=self.seed,
        )

        # Calculate elapsed time and append it to timers
        elapsed_time = time.time() - start_time
        self.timers.append(elapsed_time)
        elapsed_time_text = f"The query took {elapsed_time} seconds"

        return result, elapsed_time_text

    def ask_chat_model(self, prompt: str, model_name: str, max_tokens: int = 100):
        """
        Generate a response given a text prompt using a pre-trained language model.

        Parameters:
            prompt (str): The text prompt provided by the user.
            model_name (str): The name of the pre-trained language model to be used.
            max_tokens (int, optional): The maximum number of tokens in the generated response.
                                       Defaults to 100.

        Returns:
            tuple: A tuple containing the generated response text and the time taken for generation.

        This method loads the specified language model if it doesn't exist yet. It then utilizes the
        model to generate a response based on the provided prompt. The length of the response is
        controlled using the `max_tokens` parameter. The generated response and the time taken for
        text generation are returned as a tuple.
        """
        # Record the starting time for performance measurement
        start_time = time.time()

        # Load the model if doesn't exist yet
        if model_name not in self.models.keys():
            if self.verbose:
                print(f'Loading Model ({model_name}) for task Chat...')

            self.models = {model_name: ChatLLM(model_name, self.verbose)}

        # Generate text based on the provided prompt
        result = self.models[model_name].infer(
            prompt,
            max_tokens=max_tokens,  # Limit the length of the generated text
            seed=self.seed,
        )

        # Calculate the time taken for text generation
        elapsed_time = time.time() - start_time
        self.timers.append(elapsed_time)
        elapsed_time_text = f"The query took {elapsed_time} seconds"

        # Return the generated text and the time taken
        return result, elapsed_time_text

    def gen_image_model(self, prompt: str, model_name: str):
        """
        Generate a image given a text prompt using a pre-trained model.

        Parameters:
            prompt (str): The text prompt provided by the user.
            model_name (str): The name of the pre-trained model to be used.

        Returns:
            tuple: A tuple containing the generated image and the time taken for generation.

        This method loads the specified model if it doesn't exist yet. It then utilizes the
        model to generate a image based on the provided prompt. The generated image and the
        time taken for image generation are returned as a tuple.
        """
        # Record the starting time for performance measurement
        start_time = time.time()

        # Load the model if it doesn't exist yet
        if model_name not in self.models.keys():
            if self.verbose:
                print(f'Loading Model ({model_name}) for task Image Generation...')

            self.models[model_name] = ImageGenModel(model_name, self.verbose)

        # Perform inference with the specified model
        result = self.models[model_name].infer(
            prompt,
            seed=self.seed,
        )

        # Calculate elapsed time and append it to timers
        elapsed_time = time.time() - start_time
        self.timers.append(elapsed_time)
        elapsed_time_text = f"The query took {elapsed_time} seconds"

        return result, elapsed_time_text
