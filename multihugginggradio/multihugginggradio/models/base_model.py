import torch
from transformers import pipeline


class BaseModel():
    def __init__(
        self,
        model_name: str,
        verbose: bool = False,
    ):
        """
        Initialize a Base Model class using the Hugging Face Transformers library.

        Parameters:
            model_name (str): The name or path of the pre-trained language model to be used.
            verbose (bool): Flag to display debug prints. Defaults to False.

        This class wraps the Hugging Face `pipeline` function to create an instance of the BaseModel.
        The pipeline allows for easy text generation, completion, summarization, and other NLP tasks
        using pre-trained models. The `BaseModel` class provides a convenient interface for using the pipeline.

        Example usage:
        ```
        model = BaseModel()
        output = model.model("Text prompt...")
        print(output)
        ```
        """
        self.model = pipeline(
            model=model_name,            # Model to be used
            torch_dtype=torch.bfloat16,  # Specify the data type for PyTorch tensors
            trust_remote_code=True,      # Allow running remote code (if applicable)
            device_map="auto",           # Automatically select the device for computation
        )
        self.verbose = verbose
