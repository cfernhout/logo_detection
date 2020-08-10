import io
import cv2
import sys
from PIL import Image
import numpy as np
from flask import Flask, request, jsonify
from imageai.Detection.Custom import CustomObjectDetection

MODEL_PATH = "../models/" + sys.argv[1]
JSON_PATH = "../json/" + sys.argv[2]

app = Flask(__name__)

dtc = CustomObjectDetection()
dtc.setModelTypeAsYOLOv3()
dtc.setModelPath(MODEL_PATH)
dtc.setJsonPath(JSON_PATH)
dtc.loadModel()


def detect_objects(img, min_prob=30):
    """Processes and transforms product images to detect objects learned
    by the model loaded in global.

    Arguments:
        img {FileStorage} -- Uploaded image file though api request.

    Keyword Arguments:
        min_prob {int} -- Threshold probability for objects detected in
        images. Low probability levels show more detections
        (default: {30}).

    Returns:
        list -- List of dictionaries containing information per detected
        object in an image.
    """

    # b'\xff\xd8\xff\xe0\x00\x10...'
    image_bytes = img.read()

    # Open image as np array and change to rbg
    img_tmp = np.array(Image.open(io.BytesIO(image_bytes)))
    image = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2RGB)

    detections = dtc.detectObjectsFromImage(
        input_image=image,
        input_type="array",
        output_type="array",
        minimum_percentage_probability=min_prob,
    )

    return detections


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":

        # Read and convert image to desired shape
        img_file = request.files["file"]

        # Print detections and parse to json
        detections = detect_objects(img=img_file)[1]
        print(detections)
        return jsonify(detections)


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
