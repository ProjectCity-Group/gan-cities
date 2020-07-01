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

        self.mapData = None

        self.critic = None
        self.generator = None
        self.gan = None

        self.numChannels = 3

        self.mapDimensions = (128, 128, 3)

    def initialize(self):
        self.__initializeGenerator()
        self.__initializeDiscriminator()

        self.discriminator.trainable = False
        self.gan = Sequential()
        self.gan.add(self.generator)
        self.gan.add(self.discriminator)
        self.gan.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.0002))

    def train(self, numEpochs=500, batchSize=128):
        batchesPerEpoch = int(self.mapData.shape[0] / batchSize)
        for i in range(numEpochs):
            for j in range(batchesPerEpoch):
                numSamples = int(batchSize / 2)
                self.discriminator.train_on_batch(self.getRealMaps(numSamples), np.ones((numSamples, 1)))
                self.discriminator.train_on_batch(self.generateMapSamples(numSamples), np.zeros((numSamples, 1)))

                xGan = self.generateLatentPoints(batchSize)
                yGan = np.ones((batchSize, 1))

                generatorLoss = self.gan.train_on_batch(xGan, yGan)
            self.generator.save(f'models/epoch_{i}')

    def loadModel(self, file):
        """
        Load model
        """
        self.generator = load_model(file)
        self.generator.compile()

    def loadMapsFromDir(self, dirName):
        data = []
        for dataPath in glob.glob(f'data/{path}/*.png'):
            data = imageio.imread(imagePath)
            data.append(data)

        self.mapData = np.array(data)
        self.mapData = mapRangeToRange(self.mapData, [0, 255], [-1, 1])

    def loadMapsFromNpy_(self, file):
        """
        Load map training data from numpy file.
        """
        self.mapData = np.load(file)
        self.mapDimensions = self.mapData[0].shape

    def generateMap(self):
        latent = self.__generateLatentPoints(1)
        maps = self.generator.predict(latent)
        maps = mapRangeToRange(maps, [-1, 1], [0, 255]).astype(int)
        return maps[0]

    def saveGeneratedMap(self, imageData, fileName):
        imageio.imwrite(fileName, imageData)

    def __initializeDiscriminator(self):
        discriminatorInput = Input(shape=self.mapDimensions)

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

    def __generateLatentPoints(self, numSamples):
        xInput = randn(self.latentDimensions * numSamples)
        xInput = xInput.reshape(numSamples, self.latentDimensions)
        return xInput

    def __generateMapSamples(self, num=1, mapRange=True):
        latent = self.generateLatentPoints(num)
        maps = self.generator.predict(latent)
        if mapRange:
            maps = mapRangeToRange(maps, [-1, 1], [0, 1])
        return maps

    def __getRealMaps(self, numSamples):
        idx = randint(0, self.mapData.shape[0], numSamples)
        x = self.mapData[idx]
        y = np.ones((numSamples, 1))
        return x, y
