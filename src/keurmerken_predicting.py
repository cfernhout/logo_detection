import os
from pathlib import Path
from imageai.Detection.Custom import CustomObjectDetection

# Your data and model directories here
MODEL_PATH = "../models/planetproof_027_3288.h5"
JSON_PATH = "../models/detection_config_027.json"
IMAGE_DIR = "../data/test_images/"
RESULTS_DIR = "../data/test_results/"


def keurmerk_predict(print_results=False, min_prob=30):
    """Predicts labels with trained model files stored in ../models.

    Keyword Arguments:
        print_results {bool} -- Optional print feedback of predicted labels
        (default: {False}).
    """

    # Model path variables
    dtc = CustomObjectDetection()
    dtc.setModelTypeAsYOLOv3()
    dtc.setModelPath(MODEL_PATH)
    dtc.setJsonPath(JSON_PATH)
    dtc.loadModel()

    for f in os.listdir(IMAGE_DIR):
        # Detect object in input image
        detections = dtc.detectObjectsFromImage(input_image=IMAGE_DIR + f,
                                                output_image_path=RESULTS_DIR + f,
                                                minimum_percentage_probability=min_prob)

        # Print detection results detected in input image
        if print_results is True:
            for detection in detections:
                print(f+"\n",
                      detection["name"], ":",
                      detection["percentage_probability"], ":",
                      detection["box_points"])


if __name__ == "__main__":
    keurmerk_predict(print_results=True)
