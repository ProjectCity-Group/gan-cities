import imageio
import numpy as np
import glob
import tensorflow as tf
import pickle
import dnnlib
import dnnlib.tflib as tflib

# Wrapper class to provide loading functions for the map model
class CityGan:
    def __init__(self):
        # Initialize tensorflow
        tflib.init_tf()
        pass

    def loadModel(self, filePath):
        """
        Load a pre-trained model in pkl format.
        Args:
            filePath: The location of the model
        """
        stream = open(filePath, 'rb')
        tflib.init_tf()
        with stream:
            self.generator = pickle.load(stream, encoding='latin1')[2]
            # Generate first map to improve performance on subsequent generations
            self.generateMap()

    def generateMap(self):
        """
        Generate a map in uint8 RGB format
        """
        args = dnnlib.EasyDict()
        args.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)

        rnd = np.random.RandomState()
        latent = rnd.randn(1, self.generator.input_shape[1])

        images = self.generator.run(latent, None, **args)
        return images[0]

    def saveGeneratedMap(self, imageData, fileName):
        """
        Save a map in uint8 RGB format
        """
        imageio.imwrite(fileName, imageData)
