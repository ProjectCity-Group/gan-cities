from tensorflow import keras
import numpy
import os
import pathlib


class pix2pix_citygen():
    #pix2pix city generator class

    def __init__(self):
        #loads the model  /models/pix2pix_citygen.h5
        try:
            self.__model = keras.models.load_model(
                (pathlib.Path(__file__).parent /
                 "../gan-cities/models/pix2pix_citygen.h5").resolve())
            pass
        except:
            print(
                "load model did not work. Check if model is in CitygenModel.")
            pass

    def loadImage(self, folder: str):
        """
		loads an image and returns a numpy array and sets the array to an internal var
		Args:
		  folder: Folder in which training maps are contained
		Return:

		"""
        img = keras.preprocessing.image.load_img(folder,
                                                 target_size=(256, 256))
        img = keras.preprocessing.image.img_to_array(img)
        img = (img - 127.5) / 127.5
        img_plus = numpy.expand_dims(img, 0)
        self.__input_pic = img_plus
        return img

    def genImage(self):
        """
		generates an image from __input_pic
		Return:
			img: an numpy array
		"""
        img = self.__model.predict(self.__input_pic)
        img = (img + 1) / 2.0
        img = numpy.squeeze(img, 0)
        return img

    def saveImage(self, img, folder: str):
        """
		saves a numpy array to folder
		Args:
			img: an numpy array
			folder: Folder for saving the numpy array
		"""
        img = keras.preprocessing.image.array_to_img(img)
        keras.preprocessing.image.save_img(folder, img)
