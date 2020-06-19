class CityGenerator():
  """
  City generator class
  """

  def train(self, folder: str) -> None:
    """
    Train the generator given a set of training maps
    Args:
      folder: Folder in which training maps are contained
    """
    print(folder)

  def setHeightmap(self, map: list) -> None:
    """
    Load a PNG heightmap representing terrain to generate a city on top of.

    Args:
      map: A list of integers representing a black and white heightmap ranging from 0-255
    """
    pass

  def getParams(self) -> dict:
    """
    Get parameters currently associated with the generator
    """
    pass

  def setCountryStyle(self, country: str) -> None:
    """
    Generate a city emulating the style of cities from a given country
    Args:
      country: The country name
    """
    pass

  def getValidCountries(self) -> list:
    """
    Return a list of countries whose cities the generator was trained on

    Return:
      List[str]: List of countries names
    """
    return ['USA', 'Taiwan']

  def setCityPop(self, pop: int) -> None:
    """
    Set the population of the generated city
    Args:
      pop: The city population
    """
    pass

  def setDimensions(self, width: int, height: int) -> None:
    """
    Set the dimensions of the generated city image
    Args:
      width: The width of the generated PNG image
      height: The height of the generated PNG image
    """
    pass

  def generatePng(self) -> list:
    """
    Generate a PNG map of given size

    Returns:
      A list of integers representing pixel values in RGBA format
    """
    pass
