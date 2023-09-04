import torch

from transformers import ViTImageProcessor, ViTForImageClassification


class ImageClassModel:
    def __init__(
        self,
        model_name: str = 'google/vit-base-patch16-224',
        verbose: bool = False,
    ):
        """
        Initialize an image classification model.

        Args:
            model_name (str): The name or path of the pre-trained model to load.
            verbose (bool): Whether to enable verbose mode for debugging (default is False).
        """
        # Initialize the ViT image processor and model
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = ViTForImageClassification.from_pretrained(model_name)
        self.verbose = verbose

    def infer(self, image, seed: int = 33):
        """
        Perform inference on an input image using the initialized image classification model.

        Args:
            image: The input image(s) to classify.
            seed (int): Random seed for reproducibility (default is 33).

        Returns:
            str: The predicted class label for the input image.
        """
        # Set the random seed for reproducibility
        torch.manual_seed(seed)

        # Preprocess the input image and obtain model predictions
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()

        # Map the class index to the corresponding label and return it
        return self.model.config.id2label[predicted_class_idx]
