"""
download the model and put it in the folder logo_detection/model/
model --> https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5

download the data and put the folders [train, validation, test] in the folder logo_detection/data/
data (e.g.) --> http://qm-import-export.s3.amazonaws.com/keurmerken-od-data-students-1.zip
"""

from imageai.Detection.Custom import DetectionModelTrainer

# Your data and model directories here
DATA_DIR = "../data/"
MODEL_PATH = "../models/pretrained-yolov3.h5"


def keurmerk_train(data, model):
    """Trains YOLOv3 model from pretrained model.

    Arguments:
        data {string} -- Directory where the image and annotation data is
        stored according to the specified structure.

        model {string} -- Directory where the chosen model is stored.
    """

    # Set model type
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()

    labels = [
        "fairtrade",
        "planetproof",
        "utz",
        "organic",
        "vegan",
        "weidemelk",
        "bio",
        "eko",
        "asc",
        "msc",
        "ebio",
        "beterleven",
    ]

    # Data folder
    trainer.setDataDirectory(data_directory=DATA_DIR)

    # Training configuration
    trainer.setTrainConfig(
        object_names_array=labels,
        batch_size=4,
        num_experiments=100,
        train_from_pretrained_model=MODEL_PATH,
    )

    trainer.trainModel()


if __name__ == "__main__":
    keurmerk_train(DATA_DIR, MODEL_PATH)
