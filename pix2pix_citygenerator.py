from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from numpy import load
from numpy import expand_dims
class pix2pix_citygen():
	#pix2pix city generator class
	__filename_model = ".\gan-cities\CityGenModel\g_model_040440.h5"
	__model
	__input_pic
	def __init__(self):
		#loads the model
		self.__model = load_model(self.__filename_model)
	def loadImage(self, folder: str) -> img:
		"""
		loads an image and returns a numpy array and sets the array to an internal var
		Args:
		  folder: Folder in which training maps are contained\
		Return:

		"""
		img = load_img(filename, target_size=(256,256))
		img = img_to_array(img)
		img = (img - 127.5) / 127.5
		img = expand_dims(img, 0)
		self.__input_pic = img
		return img

	def genImage(self) -> img:
		"""
		generates an image from __input_pic
		Return:
			img: an numpy array
		"""
		img = self.__model.predict(self.__input_pic)
		return img