import torch
from diffusers import DiffusionPipeline


class ImageGenModel:
    def __init__(
        self,
        model_name: str,
        verbose: bool = False,
    ):
        """
        Initialize an ImageGenModel class using the Diffusers library.

        Parameters:
            model_name (str): The name or path of the pre-trained image generation model to be used.
            verbose (bool): Flag to display debug prints. Defaults to False.

        This class wraps the Diffusers `DiffusionPipeline.from_pretrained` function to create an instance of the
        ImageGenModel. The pipeline allows for easy image generation using pre-trained models from Diffusers. The
        `ImageGenModel` class provides a convenient interface for using the image generation pipeline.

        Example usage:
        ```
        model = ImageGenModel(model_name="CompVis/stable-diffusion-v1-4")
        output = model.model("Text prompt...")
        print(output)
        ```
        """
        self.model = DiffusionPipeline.from_pretrained(
            model_name,                  # Model to be used from Diffusers
            torch_dtype=torch.bfloat16,  # Specify the data type for PyTorch tensors
            device_map="auto",           # Automatically select the device for computation
            offload_folder="offload",    # Folder to offload the model if needed
        )
        self.verbose = verbose

    def infer(self, prompt: str, guidance_scale: float = 8.5, seed: int = 33):
        """
        Generate an image based on a text prompt using the pre-trained image generation model.

        Parameters:
            prompt (str): The text prompt provided by the user.
            guidance_scale (float): The scale factor for guidance in image generation. Defaults to 8.5.
            seed (int): The seed to be used in the inference. Defaults to 33.

        Returns:
            PIL.Image.Image: The generated image.

        The `guidance_scale` parameter controls the level of
        guidance in image generation. The `seed` parameter sets the random seed for reproducibility.

        Example usage:
        ```
        model = ImageGenModel(model_name="CompVis/stable-diffusion-v1-4")
        image = model.infer(prompt="A description of the desired image.")
        ```
        """
        # Set the random seed for reproducibility
        torch.manual_seed(seed)

        # Generate an image using the image generation model
        result = self.model(prompt, guidance_scale=guidance_scale)

        return result["images"][0]

    def release(self):
        """
        Release resources associated with the model.
        """
        del self.model
        del self.verbose
