from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="../data/")
metrics = trainer.evaluateModel(
    model_path="../models/detection_model-ex-015--loss-0004.540.h5",
    json_path="../json/detection_config.json",
    iou_threshold=0.5,
    object_threshold=0.3,
    nms_threshold=0.5,
)
print(metrics)
