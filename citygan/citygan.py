import imageio
import numpy as np
import glob
import tensorflow as tf
import pickle
import dnnlib
import dnnlib.tflib as tflib

# Implementation of a GAN to produce maps
class CityGan:
    def __init__(self):
      tflib.init_tf()
      pass

    def initialize(self):
        """
        Set up and compile the GAN - should be called before training on a set of data.
        """
        #defaultModelPath = 'models/citygan.pkl'
        #self.loadModel(defaultModelPath)
        pass

    def loadModel(self, filePath):
        """
        Load a keras model
        Args:
            filePath: The location of the model
        """
        with open(filePath, "rb") as f:
          print(filePath)
          _G, _D, self.__generator = pickle.load(f)

    def generateMap(self):
        """
        Generate a map in uint8 RGB format
        """
        rnd = np.random.RandomState(5)
        latent = rnd.randn(1, generator.input_shape[1])

        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = generator.run(latent, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

        return images[0]

    def saveGeneratedMap(self, imageData, fileName):
        """
        Save a map in uint8 RGB format
        """
        imageio.imwrite(fileName, imageData)

    def __generateLatentVector(self, numSamples):
        """
        Generates a random latent space vector to be fed into the generator
        """
        xInput = randn(self.latentDimensions * numSamples)
        xInput = xInput.reshape(numSamples, self.latentDimensions)
        return xInput
