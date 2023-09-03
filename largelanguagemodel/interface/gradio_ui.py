import time
import gradio as gr

from largelanguagemodel.models.chat_llm import ChatLLM
from largelanguagemodel.utils.config.config import UIConfig


class GradioApp(object):
    def __init__(
        self,
        model_config: str = 'chat_config.yaml',
    ):
        """
        Initialize a GradioApp for interacting with a language model.

        Parameters:
            model_config (str): Path to the configuration file for the GradioApp and model settings.
                               Defaults to 'chat_config.yaml'.

        This class sets up a graphical interface using the Gradio library to interact with a
        language model for various tasks. It loads configuration settings from the specified
        `model_config` file, including available models, task type, and reproducibility settings.
        """
        self.config = UIConfig.get_config(model_config)
        self.available_models = self.config['AVAILABLE_MODELS']
        self.task = self.config['TASK']
        self.seed = self.config['REPRODUCIBILITY']['SEED']
        self.verbose = self.config['VERBOSE']

        self.model = None

        self.timers = []

    def run(self):
        """
        Launch the GUI interface for interacting with the language model.

        This method creates a Gradio interface using the `ask_model` function to generate
        responses based on user input prompts. Users can select a model from the available
        models and provide a text prompt. The generated response and the time taken for
        text generation are displayed.
        """

        # Create a Gradio interface using the Blocks context
        with gr.Blocks(title="ContiGPT") as self.demo:
            with gr.Row():
                with gr.Column():
                    # Create a textbox for the user to input a question
                    question = gr.Textbox(label="Question")

                    # Create a dropdown menu for the user to select a model
                    select_model = gr.Dropdown(self.available_models, label="Models", value=self.available_models[0])

                    gr.Examples(examples=["How do you say \"Hello\" in portuguese?", "Now say it in spanish"],
                                inputs=[question])

                with gr.Column():
                    # Create a textbox to display the generated answer
                    answer = gr.Textbox(label="Answer")

                    # Create a textbox to display the elapsed time for text generation
                    elapsed_time = gr.Textbox(label="Elapsed Time")

            # Create a submit button
            submit = gr.Button("Submit")

            # Create a clear button to reset the input fields
            gr.ClearButton([question, answer, elapsed_time])

            # Define the behavior when the submit button is clicked
            submit.click(fn=self.ask_model, inputs=[question, select_model], outputs=[answer, elapsed_time])

        # Launch the Gradio interface with the defined components
        self.demo.launch(share=False)

        # Close the Gradio interface when finished
        self.demo.close()

    def ask_model(self, prompt: str, model_name: str, max_tokens: int = 100):
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
        if self.model is None or model_name not in self.model.keys():
            if self.verbose:
                print(f'Loading Model ({model_name}) for task {self.task}...')

            if self.task == 'Chat':
                self.model = {model_name: ChatLLM(model_name, self.verbose)}
            else:
                raise Exception(f'Unespected task found ({self.task})')

            if self.verbose:
                print('Loading Complete!')

        # Generate text based on the provided prompt
        result = self.model[model_name].infer(
            prompt,
            max_tokens=max_tokens,  # Limit the length of the generated text
            seed=self.seed,
        )

        # Extract the generated text from the result
        answer = result[0]["generated_text"]

        # Calculate the time taken for text generation
        elapsed_time = time.time() - start_time
        self.timers.append(elapsed_time)
        elapsed_time_text = f"The query took {elapsed_time} seconds"

        # Return the generated text and the time taken
        return answer, elapsed_time_text


if __name__ == "__main__":
    gui = GradioApp(model_config='chat_config.yaml')
    gui.run()
