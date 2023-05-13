# Distracted Driver Detection System Using Deep Learning

Distracted Driver Detection System is a deep learning project which is used to detect the distracted driver. This project is based on a real life problem where
a distracted driver becomes a reason for road accidents. This causes not only the financial loss but sometimes loss of life.

This projects divided driver activities into 10 different classes which are given below:
1. Safe Driving
2. Texting right
3. Texting_on_the_phone_right
4. Texting left
5. Texting_on_the_phone_left
6. drinking
7. Operating the Radio
8. Reaching behind
9. hair-and-makeup
10. Talking to the passenger 

The project uses CNN(Convolutional Neural Networks) to classify the images.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Datasets](#DataSet)
- [Deep Learning Model Used](#Deep-Learning-Model-Used)
- [Python Dependencies](#PythonDependencies)
- [Credits](#credits)

## Installation

To install this project, follow these steps:

1. Clone the repository
2. Install the required packages using pip
pip install -r requirements.txt


## Usage

To use this project, follow these steps:
Before running the project, you need the model and place the model into the "static/deep_learning_projects".
The name of the model file should be: cnn_model.h5
1. Run the following command:
python main.py


## DataSet
For this project, We've used 2 Datasets:
1. sarahh222/distracteddriversrevampeddataset
2. rajeevsharma993/distracted-driver-dataset

These datasets consists of images from the classes above.

## Deep-Learning-Model-Used

This project is based on CNN(Convolutional Neural Network model). Below is the description of layers.

The model has two convolutional (Conv2D) layers. Specifically, the model has the following layers:

1. Input layer (Conv2D): 16 filters with a kernel size of 3x3 and a Rectified Linear Unit (ReLU) activation function.
2. MaxPooling2D: with a pool size of 2x2
3. Conv2D: 32 filters with a kernel size of 3x3 and a ReLU activation function.
4. MaxPooling2D: with a pool size of 2x2
5. Flatten layer
6. Dense layer: with 64 units and a ReLU activation function.
7. Dropout layer: with a rate of 0.2
8. Dense layer: with 32 units and a ReLU activation function.
9. Dropout layer: with a rate of 0.2
10. Output layer (Dense): with 10 units and a softmax activation function.


## PythonDependencies:
pandas
matplotlib
tensorflow
keras
numpy
Flask
flask-mysqldb
pymysql

## Install Dependencies (requirements.txt)
pip install -r requirements.txt

## Credits

This is a team based project created by: - 
1. Lalit Dungriyal
2. Himanshu Pal
3. Amit Gussain
4. Arvind Rawat
