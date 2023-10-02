import torch
import os
import sys
import pathlib
import numpy as np
from PIL import Image, ImageChops
from multihugginggradio.models.image_gen_model import ImageGenModel


class TestImageClassModel:
    @classmethod
    def setup_class(cls):
        """
        Set up test resources and create an instance of the ImageClassModel class for testing.

        This class method is used to set up resources required for testing and to create an instance of
        the ImageClassModel class. It initializes attributes like the model name and expected response for later use.
        """

        file_path = pathlib.Path(__file__).parent.resolve()

        image_path = os.path.join(file_path, 'resources', 'mock_image_generation_output.png')
        cls.expected_image = Image.open(image_path)

        image_ghactions_path = os.path.join(file_path, 'resources', 'mock_image_generation_output_ghactions.png')
        cls.expected_image_ghactions = Image.open(image_ghactions_path)

        cls.model_name = 'CompVis/stable-diffusion-v1-4'
        cls.model = ImageGenModel(cls.model_name)

    def test_inference_output(self):
        """
        Test the output of the image generatioon model's inference method.

        This method performs a test on the inference method of the ImageGenModel class. It generates a response
        based on a prompt and asserts whether the generated image matches the expected image. If the
        assertion fails, it indicates an unexpected image from the model.
        """

        # Prompt for image generation inference
        image_generation_prompt = "Pagani-like Sports Car"

        # Perform inference on the model
        generated_image = self.model.infer(image_generation_prompt, seed=33)

        np.set_printoptions(threshold=sys.maxsize)
        print(np.array(generated_image))
        generated_image.save(os.path.join(pathlib.Path(__file__).parent.resolve(), 'resources', 'mock_image_generation_output_ghactions.png'))

        if sys.platform == "win32":  # Check locally (only on gpu)
            are_images_equal = not ImageChops.difference(generated_image, self.expected_image).getbbox(),
            assert are_images_equal, 'Failed! Unexpected generated image!'
        else:  # Check on github actions workflow
            are_images_equal = not ImageChops.difference(generated_image, self.expected_image_ghactions).getbbox()
            assert are_images_equal, 'Failed! Unexpected generated image!'
        
        torch.cuda.empty_cache()
