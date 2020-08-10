# Keurmerken - Object Detection

## 

The goal of this project is to detect quality marks on food products. In order to use the code in this repository, some steps have to be taken.

## 1. Data & file structure

Image data data needs to be labelled in .xml format. The LabelImg tool (https://github.com/tzutalin/labelImg) can be used to do so.

To train and validate your model a training and validation set is needed, both containing a folder with the images and the belonging annotations. Your data structure should look like this:

```
├── train
│   ├── annotations
│   │   ├── image_1.xml
│   │   └── image_2.xml
│   └── images
│       ├── image_1.jpg
│       └── image_2.jpg
└── validation
    ├── annotations
    │   ├── image_3.xml
    │   └── image_4.xml
    └── images
        ├── image_3.jpg
        └── image_4.jpg
```
## 2. Installing 

Conda users install dependencies using the yml file included.
```bash
$ conda env create -f environment.yml
```

Otherwise, using pip.
```bash
$ pip install -r requirements.txt
```

## 3. Training and finetuning

Besides the training and validation, you need a pretrained network. We used yolov3 (stored in .h5 format) to train the model. This model can be downloaded by cloning the following github repo: 
https://github.com/qqwweee/keras-yolo3.

By running the following command the weights are transformed into a .h5 file, which will be used for training. 

```console
$ python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
```


In order to train your model, transfer learning will be used from the pretrained yolo network.

```keurmerken_training.py```
- DATA_DIR =  path to your data folder containing train and validation set
- MODEL_PATH =  path to your pretrained model (i.e. yolov3.h5) stored in .h5 format
- labels = list with the labels of your annotations


```keurmerken_predicting.py```:

- MODEL_PATH =  path to your model after training (automatically stored in the map models)
- JSON_PATH = path to the .json file created while training (automatically stored in the map json)
- IMAGE_DIR =  directory where the images you want to predict the label on are stored
- RESULTS_DIR =  directory where the images after they are annotated and labelled should be stored

While training the model will automatically create a ```cache```, ```logs``` and ```json``` folder in root. The ```models``` folder contains the models made while training and saves automatically if it performs better than the latest step.

If you want to change something, for instance the labels, you should delete the ```cache```, ```logs``` and the ```json``` folders in order to retrain your model. This is an unfortunate quirk that is part of the ImageAI library.

### 3.1. tl:dr -- adding new labels

1. Remove ```cache```, ```json``` and ```logs``` folders from your data directory.
2. Label new data and store in the ```training``` and ```validation``` folders.
3. Add the new label to the list of labels in the ```keurmerken_training.py``` file.
4. Retrain your model.

## 4. API

A small API service is built on Flask and will expect one image as a request for quality mark detection.

Similar to model training, model and model settings files need to be specified in order to start. This can be done in-file or as command line arguments.

In the ```/api``` folder, run:
```bash
python app.py your_model.h5 your_model_config.json
```