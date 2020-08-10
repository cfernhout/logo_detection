from imageai.Detection.Custom import DetectionModelTrainer

def main():
    """
    model --> https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5
    """
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

    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="../data")
    trainer.setTrainConfig(object_names_array=labels, batch_size=4,
                           num_experiments=3, train_from_pretrained_model="../models/pretrained-yolov3.h5")
    trainer.trainModel()

if __name__ == "__main__":
    main()