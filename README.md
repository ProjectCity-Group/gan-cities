# GAN Cities Generator

A procedural city generator using generative adversarial networks.

## Usage

### Using the pre-built model
```python
cityGan = CityGAN()
cityGan.loadModel('models/citygan')

cityMap = cityGan.generateMap()
```

### Training the model with your own data
```python
cityGan = CityGAN()
cityGan.initialize()
cityGan.loadMapsFromDir('maps')

cityGan.train()
cityMap = cityGan.generateMap()
```

## GUI
If on Windows, installing GTK via instructions provided here https://www.gtk.org/docs/installations/windows/
should be sufficient along with installing pycario and PyGObject froom pip. 

Full documentaiton on installing PyGobject can be found here: https://pygobject.readthedocs.io/en/latest/getting_started.html
![Screenshot of GanCities UI](https://raw.githubusercontent.com/ProjectCity-Group/gan-cities/master/screenshot/screenshot.png?token=ACHD5QBWEP3NRK2SNS6QEAK667B3O)
