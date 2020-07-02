# GAN Cities Generator

A procedural city generator using generative adversarial networks.

**NOTE**: In order to successfully clone this repository, Git LFS is required.
After installing Git LFS and cloning this repository, run `git lfs pull`
in order to ensure that the models are successfully downloaded.

## Usage

### Using the pre-built model
```python
from citygan import CityGan 

cityGan = CityGan()
cityGan.loadModel('models/citygan')

cityMap = cityGan.generateMap()
```

### Training the model with your own data
```python
from citygan import CityGan

cityGan = CityGan()
cityGan.initialize()
cityGan.loadMapsFromDir('maps')

cityGan.train()
cityMap = cityGan.generateMap()
```

## GUI
This library comes with a GUI demonstrating features of the library. Simply run `gui.py`.

If on Windows, installing GTK via instructions provided here https://www.gtk.org/docs/installations/windows/
should be sufficient along with installing pycairo and PyGObject from pip. 

Full documentation on installing PyGObject can be found here: https://pygobject.readthedocs.io/en/latest/getting_started.html
![Screenshot of GanCities UI](https://raw.githubusercontent.com/ProjectCity-Group/gan-cities/master/screenshot/screenshot.png?token=ACHD5QBWEP3NRK2SNS6QEAK667B3O)

## GAN Models

The developer generated GAN files are included in the github repository, but not in the PyPi Package. 
If you downloaded from PyPi you must also download the model files. The pix2pix model can be found [here](https://github.com/ProjectCity-Group/gan-cities/blob/master/citygan/models/pix2pix_citygen.h5?raw=true) and the CityGan model can be found [here](https://github.com/ProjectCity-Group/gan-cities/tree/master/citygan/models/citygan). The file structure should match what you see in the git repository. 
