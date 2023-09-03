import torch
from multihugginggradio.models.base_llm import LLM


class ChatLLM(LLM):
    def __init__(
        self,
        model_name: str = 'databricks/dolly-v2-3b',
        verbose: bool = False,
    ):
        """
        Initialize a Chat_LLM class based on a pre-existing LLM (Language Model) class.

        Parameters:
            model_name (str): The name or path of the pre-trained language model to be used.
                              Defaults to 'databricks/dolly-v2-3b'.
            verbose (bool): Flag to display debug prints. Defaults to False.

        This class is derived from the base LLM class and is specifically tailored for chat-like
        interactions using a pre-trained language model. It inherits the capabilities of the LLM class
        and extends it with a custom `infer` method for generating responses to given prompts.

        Example usage:
        ```
        chat_llm = Chat_LLM()
        response = chat_llm.infer("User: Hello!", max_tokens=50, seed=33)
        print(response)
        ```
        """
        super().__init__(model_name=model_name, verbose=verbose)

        self.conversation_history = []

    def infer(self, prompt: str, max_tokens: int = 100, seed: int = 33):
        """
        Generate a response given a text prompt using the pre-trained language model.

        Parameters:
            prompt (str): The text prompt provided by the user.
            max_tokens (int): The maximum number of tokens in the generated response. Defaults to 100.
            seed (int): The seed to be used in the inference. Defaults to 33.
        Returns:
            list: The generated output.

        This method utilizes the inherited `model` attribute from the base LLM class to generate a
        response based on the provided prompt. The `max_new_tokens` parameter is set to control the
        length of the response. The generated response is returned as a string.
        """
        # Set the random seed for reproducibility
        torch.manual_seed(seed)

        # Add the current user prompt to the conversation history
        self.conversation_history.append(prompt)

        # Combine all conversation history into a single prompt
        conversation_prompt = "\n".join(self.conversation_history)

        # Print conversation input if verbose mode is enabled
        if self.verbose:
            print(f'Conversation input:\n"""\n{conversation_prompt}\n"""')

        # Generate a response using the language model
        result = self.model(conversation_prompt, max_new_tokens=max_tokens)

        # Add the generated response to the conversation history
        self.conversation_history.append(result[0]["generated_text"])

        return result
