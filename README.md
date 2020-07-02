# GAN Cities Generator

A procedural city generator using generative adversarial networks.

**NOTE**: In order to successfully clone this repository, Git LFS is required.
After installing Git LFS and cloning this repository, run `git lfs pull`
in order to ensure that the models are successfully downloaded.

## Usage

### Using the pre-built model
```python
from citygan.citygan import CityGan 

cityGan = CityGan()
cityGan.loadModel('models/citygan')

cityMap = cityGan.generateMap()
```

### Training the model with your own data
```python
from citygan.citygan import CityGan

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
