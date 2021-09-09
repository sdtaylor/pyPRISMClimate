from setuptools import setup, find_packages

# Set the version number in pyPRISMClimate/version.py
version = {}
with open('pyPRISMClimate/version.py') as fp:
    exec(fp.read(), version)
VERSION = version['__version__']

LONG_DESCRIPTION = """
# pyPRISMClimate

An interface to the PRISM Climate data with functions similar
to the R package [prism](https://github.com/ropensci/prism)

## Installation

Requires python 3. No other packages needed.

Install via pip
```
pip install pyPRISMClimate
```

Install the latest version directly from GitHub:
```
pip install git+git://github.com/sdtaylor/pyPRISMClimate
```

## Documentation

[https://sdtaylor.github.io/pyPRISMClimate](https://sdtaylor.github.io/pyPRISMClimate)

## Acknowledgments

Development of this software was funded by
[the Gordon and Betty Moore Foundation's Data-Driven Discovery Initiative](http://www.moore.org/programs/science/data-driven-discovery) through
[Grant GBMF4563](http://www.moore.org/grants/list/GBMF4563) to Ethan P. White.
"""

setup(name='pyPRISMClimate',
      version=VERSION,
      description='An interface to the PRISM Climate data',
      long_description = LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='https://github.com/sdtaylor/pyPRISMClimate',
      author='Shawn Taylor',
      license='MIT',
      python_requires='>=3.6.0',
      packages=find_packages(),
      zip_safe=False)
