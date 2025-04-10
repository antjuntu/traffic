import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    print(tf.__version__)
    #python traffic.py gtsrb
    # Check command-line arguments
    # TODO
    # if len(sys.argv) not in [2, 3]:
    #     sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    #images, labels = load_data(sys.argv[1])
    images, labels = load_data('gtsrb')
    print(len(images), len(labels))

    
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")
    


def load_data(data_dir):
    print('data_dir', data_dir)
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    root = os.getcwd()
    print('root', root)
    directory_str = os.path.join(root, data_dir)
    directory = os.fsencode(directory_str)
    for folder in os.listdir(directory):
        foldername = os.path.basename(folder)
        #print('foldername', foldername)
        try:
            label = int(foldername.decode('utf8'))
        except:
            continue

        print(type(foldername), foldername, 'label(int):', label)
        inner_dir_str = os.path.join(root, data_dir, foldername.decode('utf8'))
        #print('inner_dir_str', inner_dir_str)
        inner_dir = os.fsdecode(inner_dir_str)
        
        for filename in os.listdir(inner_dir):
            #print('filename', type(filename), filename)
            imgPath = os.path.join(inner_dir_str, filename)
            #print('imgPath', imgPath)
            img = cv2.imread(imgPath)
            img_resized = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

            images.append(img_resized)
            labels.append(label)
            # if filename == '00004_00029.ppm':
            #     print('imgPath', imgPath)
            #     print(type(img), img.shape)
            #     print(img_resized.shape)
    
    # imgPath = os.path.join(root, data_dir, '0', '00000_00000.ppm')
    # print('imgPath', imgPath)
    # img = cv2.imread(imgPath)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
