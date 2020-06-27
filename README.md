# GAN Cities Generator

A procedural city generator using generative adversarial networks.

## Usage

```python
generator = CityGenerator()
generator.setHeightmap(...)
generator.setCountryStyle('USA')
generator.setPopulation(50000)
generator.setDimensions(500, 500)
city = generator.generate()
```

## GUI
If on Windows, installing GTK via instructions provided here https://www.gtk.org/docs/installations/windows/
should sufficient along with installing pycario and PyGObject froom pip. 
Full documentaiton on installing PyGobject can be found here: https://pygobject.readthedocs.io/en/latest/getting_started.html
![Screenshot of GanCities UI](https://raw.githubusercontent.com/ProjectCity-Group/gan-cities/master/screenshot/screenshot.png?token=ACHD5QBWEP3NRK2SNS6QEAK667B3O)
