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
        with open('./models/citygan.pkl', 'rb') as f:
            self.generator = pickle.load(f, encoding='latin1')[2]
            # Generate first map to improve performance on subsequent generations
            self.generate_map()

    def generate_map(self):
        """
        Generate a map in uint8 RGB format
        """
        args = dnnlib.EasyDict()
        args.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)

        rnd = np.random.RandomState()
        latent = rnd.randn(1, self.generator.input_shape[1])

        images = self.generator.run(latent, None, **args)
        return images[0]

    def save_generated_map(self, imageData, fileName):
        """
        Save a map in uint8 RGB format
        """
        imageio.imwrite(fileName, imageData)
