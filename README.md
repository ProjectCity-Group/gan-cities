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
