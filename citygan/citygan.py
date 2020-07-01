import imageio
import numpy as np
import glob
import tensorflow as tf
from tensorflow import keras

from keras import backend
from keras.models import Model
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D
from keras.layers import Input
from keras.layers import Flatten
from keras.layers import Activation
from keras.layers import Dense
from keras.layers import BatchNormalization
from keras.layers import Reshape
from keras.layers import UpSampling2D
from keras.layers import Lambda
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.layers import Conv2DTranspose
from keras.layers import AveragePooling2D
from keras.layers import ReLU

from citygan_util import mapRangeToRange

from keras.optimizers import RMSprop
from keras.optimizers import Adam

from keras.initializers import RandomNormal

from matplotlib import pyplot as plt
from numpy.random import randint
from numpy.random import randn

# Implementation of a GAN to produce maps
class CityGan:
    def __init__(self):
        self.latentDimensions = 512
        self.discriminatorLearningRate = 0.0002
        self.generatorLearningRate = 0.0002

        self.__mapData = None

        self.__critic = None
        self.__generator = None
        self.__gan = None

        self.__numChannels = 3

        self.__mapDimensions = (128, 128, 3)

    def initialize(self):
        """
        Set up and compile the GAN - should be called before training on a set of data.
        """
        self.__initializeGenerator()
        self.__initializeDiscriminator()

        self.discriminator.trainable = False
        self.gan = Sequential()
        self.gan.add(self.generator)
        self.gan.add(self.discriminator)
        self.gan.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.0002))

    def train(self, numEpochs=500, batchSize=128):
        """
        Train the GAN on a previously loaded set of data.
        Args:
            numEpochs: The number of epochs to train for
            batchSize: The size of each training batch
        """
        batchesPerEpoch = int(self.__mapData.shape[0] / batchSize)
        for i in range(numEpochs):
            for j in range(batchesPerEpoch):
                # Utilize half batch size to train discriminator
                numSamples = int(batchSize / 2)

                # Train the discriminator
                self.discriminator.train_on_batch(self.__getRealMaps(numSamples), np.ones((numSamples, 1)))
                self.discriminator.train_on_batch(self.__generateMapSamples(numSamples), np.zeros((numSamples, 1)))

                xGan = self.__generateLatentVector(batchSize)
                yGan = np.ones((batchSize, 1))

                generatorLoss = self.gan.train_on_batch(xGan, yGan)
            self.generator.save(f'models/epoch_{i}')

    def loadModel(self, filePath):
        """
        Load a keras model
        Args:
            filePath: The location of the model
        """
        self.generator = load_model(filePath)

    def loadMapsFromDir(self, dirName):
        """
        Loads training data from a directory - all maps are expected to be in PNG uint8 RGBA format
        Args:
            dirName: The location of the folder in which the maps are located
        """
        data = []
        for dataPath in glob.glob(f'data/{path}/*.png'):
            data = imageio.imread(imagePath)
            data.append(data)

        self.__mapData = np.array(data)
        self.__mapData = mapRangeToRange(self.__mapData, [0, 255], [-1, 1])

    def loadMapsFromNpy_(self, filePath):
        """
        Load map training data from numpy file
        Args:
            filePath
        """
        self.__mapData = np.load(filePath)
        self.__mapDimensions = self.__mapData[0].shape

    def generateMap(self):
        """
        Generate a map in uint8 RGB format
        """
        latent = self.__generateLatentVector(1)
        maps = self.generator.predict(latent)
        maps = mapRangeToRange(maps, [-1, 1], [0, 255]).astype(np.uint8)
        return maps[0]

    def saveGeneratedMap(self, imageData, fileName):
        """
        Save a map in uint8 RGB format
        """
        imageio.imwrite(fileName, imageData)

    def __initializeDiscriminator(self):
        """
        Set up and compile the discriminator model
        """
        discriminatorInput = Input(shape=self.__mapDimensions)

        discriminator = Conv2D(16, (3, 3), strides=(2,2), padding='same')(discriminatorInput)
        discriminator = LeakyReLU(alpha=0.2)(discriminator)

        # Downsample to 32x32
        discriminator = Conv2D(32, (3, 3), padding='same', strides=(2, 2))(discriminator)
        discriminator = LeakyReLU(alpha=0.2)(discriminator)

        # Downsample to 16x16
        discriminator = Conv2D(64, (3, 3), padding='same', strides=(2, 2))(discriminator)
        discriminator = LeakyReLU(alpha=0.2)(discriminator)

        # Downsample to 8 x 8
        discriminator = Conv2D(128, (3, 3), padding='same', strides=(2, 2))(discriminator)
        discriminator = LeakyReLU(alpha=0.2)(discriminator)

        # Downsample to 4x4
        discriminator = Conv2D(512, (3, 3), padding='same', strides=(2, 2))(discriminator)
        discriminator = LeakyReLU(alpha=0.2)(discriminator)

        discriminator = Flatten()(discriminator)
        discriminatorOutput = Dense(1, activation='sigmoid')(discriminator)

        opt = Adam(lr=0.0002, beta_1=0.5)

        self.discriminator = Model(discriminatorInput, discriminatorOutput)
        self.discriminator.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

    def __initializeGenerator(self):
        """
        Setup without compiling the generator model
        """
        PNG_DIM = 3

        startImageWidth = 4
        startImageHeight = 4
        lRluAlpha = 0.2
        genKernelSize = (3, 3)

        generatorInput = Input(shape=self.latentDimensions)
        generator = Dense(512 * startImageWidth * startImageHeight)(generatorInput)

        generator = Reshape([startImageHeight, startImageWidth, 512])(generator)

        # 4x4
        generator = Conv2D(filters=256, kernel_size=(3, 3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        # 8x8
        generator = UpSampling2D(interpolation='nearest')(generator)
        generator = Conv2D(filters=128, kernel_size=(3,3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        # 16x16
        generator = UpSampling2D(interpolation='nearest')(generator)
        generator = Conv2D(filters=64, kernel_size=(3,3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        # 32x32
        generator = UpSampling2D(interpolation='nearest')(generator)
        generator = Conv2D(filters=32, kernel_size=(3,3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        # 64x64
        generator = UpSampling2D(interpolation='nearest')(generator)
        generator = Conv2D(filters=16, kernel_size=(3, 3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        # 128 x 128
        generator = UpSampling2D(interpolation='nearest')(generator)
        generator = Conv2D(filters=16, kernel_size=(3, 3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        generator = Conv2D(filters=8, kernel_size=(3,3), padding='same')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        generatorOutput = Conv2D(filters=3, kernel_size=(1, 1), activation='tanh')(generator)
        generator = LeakyReLU(alpha=lRluAlpha)(generator)

        self.generator = Model(generatorInput, generatorOutput)
        return generator

    def __generateLatentVector(self, numSamples):
        """
        Generates a random latent space vector to be fed into the generator
        """
        xInput = randn(self.latentDimensions * numSamples)
        xInput = xInput.reshape(numSamples, self.latentDimensions)
        return xInput

    def __generateMapSamples(self, num=1, mapRange=True):
        """
        Generate map samples to feed into the discriminator
        """
        latent = self.generateLatentPoints(num)
        maps = self.generator.predict(latent)
        if mapRange:
            maps = mapRangeToRange(maps, [-1, 1], [0, 1])
        return maps

    def __getRealMaps(self, numSamples):
        """
        Get real map samples to feed into discriminator

        """
        idx = randint(0, self.__mapData.shape[0], numSamples)
        x = self.mapData[idx]
        y = np.ones((numSamples, 1))
        return x, y
