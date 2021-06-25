from setuptools import setup, find_packages

# Set the version number in pyPRISMClimate/version.py
version = {}
with open('pyPRISMClimate/version.py') as fp:
    exec(fp.read(), version)
VERSION = version['__version__']

setup(name='pyPRISMClimate',
      version=VERSION,
      description='An interface to the PRISM Climate data',
      url='https://github.com/sdtaylor/pyPRISMClimate',
      author='Shawn Taylor',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
