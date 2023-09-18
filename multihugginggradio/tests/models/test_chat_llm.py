import torch
import sys

from multihugginggradio.models.chat_llm import ChatLLM


class TestChatLLM:
    @classmethod
    def setup_class(cls):
        """
        Set up test resources and create an instance of the Chat_LLM class for testing.

        This class method is used to set up resources required for testing and to create an instance of
        the Chat_LLM class. It initializes attributes like the model name and expected response for later use.
        """
        cls.model_name = 'databricks/dolly-v2-3b'
        cls.expected_output_win_gpu = 'Hello, thank you for your inquiry! Our team is available in chat 24/7 and' \
            ' will respond to you as soon as possible!'
        cls.expected_output_win_cpu = 'Hello there! My name is Joe, and I\'m a Machine Learning engineer at' \
            ' Databricks. I help customers with their machine learning and AI problems. Let me walk you through' \
            ' the Databricks platform.'
        cls.expected_output_linux_cpu = 'Welcome to bluemix. Here are some additional helpful links: \n\n' \
            '- [Compute overview](https://www.bluemix.com/help/new-to-bluemix/computes-overview)'

        cls.model = ChatLLM(cls.model_name)

    def test_inference_output(self):
        """
        Test the output of the language model's inference method.

        This method performs a test on the inference method of the Chat_LLM class. It generates a response
        based on a prompt and asserts whether the generated response matches the expected response. If the
        assertion fails, it indicates an unexpected response from the model.
        """
        response = self.model.infer("Hello!", max_tokens=50, seed=33)

        if sys.platform == "win32":
            if torch.cuda.is_available():
                assert response == self.expected_output_win_gpu, 'Failed! Unexpected output!'
            else:
                assert response == self.expected_output_win_cpu, 'Failed! Unexpected output!'
        else:
            if torch.cuda.is_available():
                assert response == self.expected_output_linux_gpu, 'Failed! Unexpected output!'
            else:
                assert response == self.expected_output_linux_cpu, 'Failed! Unexpected output!'
