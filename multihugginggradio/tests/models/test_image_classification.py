import torch
import os
import sys
import pathlib
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
        # torch.cuda.is_available = lambda : False
        cls.model_name = 'google/vit-base-patch16-224'

        cls.expected_output_ghactions = 'Welcome to Scribd. Your first message was sent on October 5, 2023.'

        cls.expected_class_gpu = 'sports car, sport car'
        cls.expected_score_gpu = 13.56125545501709
        cls.expected_class_ghactions = 'sports car, sport car'
        cls.expected_score_ghactions = 13.56125545501709
        # print(torch.cuda.is_available())
        cls.model = ImageClassModel(cls.model_name)

    def test_inference_output(self):
        """
        Test the output of the image classification model's inference method.

        This method performs a test on the inference method of the ImageClassModel class. It generates a response
        based on a prompt and asserts whether the generated response matches the expected response. If the
        assertion fails, it indicates an unexpected response from the model.
        """
        # print(torch.cuda.is_available())
        image = Image.open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'resources', 'mock_sport_car.png'))
        image = np.array(image)[:, :, :3]
        # print(image.shape)
        predicted_class, scores = self.model.infer(image, seed=33, return_logits=True)
        score = torch.max(scores).item()
        print(predicted_class, score)
        if sys.platform == "win32":  # Check locally
            if torch.cuda.is_available():
                assert predicted_class == self.expected_class_gpu, 'Failed! Unexpected class prediction!'
                assert score == self.expected_score_gpu, 'Failed! Unexpected class score prediction!'
            else:
                assert predicted_class == self.expected_class_gpu, 'Failed! Unexpected class prediction!'
                assert score == self.expected_score_gpu, 'Failed! Unexpected class score prediction!'
        else:  # Check on github actions workflow
            assert predicted_class == self.expected_class_gpu, 'Failed! Unexpected class prediction!'
            assert score == self.expected_score_gpu, 'Failed! Unexpected class score prediction!'
