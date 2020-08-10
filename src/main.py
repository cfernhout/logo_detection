from imageai.Detection.Custom import DetectionModelTrainer

def main():
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="../data/raw/headset")
    trainer.setTrainConfig(object_names_array=["hololens", "oculus"], batch_size=32,
                           num_experiments=100, train_from_pretrained_model="../models/pretrained-yolov3.h5")
    trainer.trainModel()

if __name__ == "__main__":
    main()