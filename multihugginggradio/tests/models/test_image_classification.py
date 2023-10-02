import torch
import os
import sys
import pathlib
import gc
import numpy as np
from PIL import Image
from multihugginggradio.models.image_class_model import ImageClassModel


class TestImageClassModel:
    @classmethod
    def setup_class(cls):
        """
        Set up test resources and create an instance of the ImageClassModel class for testing.

        This class method is used to set up resources required for testing and to create an instance of
        the ImageClassModel class. It initializes attributes like the model name and expected response for later use.
        """
        cls.expected_class = 'sports car, sport car'
        cls.expected_score = 13.56125545501709
        cls.expected_class_ghactions = 'sports car, sport car'
        cls.expected_score_ghactions = 13.561249732971191

        cls.model_name = 'google/vit-base-patch16-224'
        cls.model = ImageClassModel(cls.model_name)

    def test_inference_output(self):
        """
        Test the output of the image classification model's inference method.

        This method performs a test on the inference method of the ImageClassModel class. It generates a response
        based on an image and asserts whether the generated output matches the expected output. If the
        assertion fails, it indicates an unexpected output from the model.
        """
        # Load the image for testing
        image = Image.open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'resources', 'mock_sport_car.png'))
        image = np.array(image)[:, :, :3]  # Convert image to a numpy array

        # Perform inference on the model
        predicted_class, scores = self.model.infer(image, seed=33, return_logits=True)
        score = torch.max(scores).item()  # Get the maximum score from the prediction logits

        if sys.platform == "win32":  # Check locally (only on gpu)
            assert predicted_class == self.expected_class, 'Failed! Unexpected class prediction!'
            assert score == self.expected_score, 'Failed! Unexpected class score prediction!'
        else:  # Check on github actions workflow
            assert predicted_class == self.expected_class_ghactions, 'Failed! Unexpected class prediction!'
            assert score == self.expected_score_ghactions, 'Failed! Unexpected class score prediction!'

        # Clear memory to avoid crashes
        del image
        del predicted_class
        del scores
        del score
        self.model.release()
        torch.cuda.empty_cache()
        gc.collect()
