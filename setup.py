from setuptools import setup
setup(
  name = 'citygan',
  packages = ['citygan'],
  version = '0.1.4',
  license='MIT',
  description = 'Procedurally generated cities using generative adversarial networks',
  author = 'Thomas Allen, Eric Lehmann, Jacob Roberge, Christopher Ward, Adrian Wright',
  url = 'https://github.com/ProjectCity-Group/gan-cities',
  download_url = 'https://github.com/ProjectCity-Group/gan-cities/archive/v0.1.2.tar.gz',
  keywords = ['gan', 'city', 'procedural', 'generation'],
  install_requires=[
        'wheel',
        'imageio',
        'keras',
        'matplotlib',
        'numpy',
        'tensorflow'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

