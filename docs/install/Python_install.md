# Installation of nmpccodegen on Python 3
At the moment there is no package, but very soon the python package will be available in pip.

## What do I need?
- GNU toolchain with make (more info [here](Toolchain_install.md))
- python 3 with casadi 3.2.x or higher and numpy/matplotlib installed on it
- Cmake
- Some of the demos might require aditions library's such as matplotlib to visualize the results

## How to install
- make sure Cmake,make and gcc are installed 
- git clone (with the --recursive flag on) the [nmpc-codegen-python](https://github.com/kul-forbes/nmpc-codegen-python) repo 
- add src to your python path
- !! no compilation is required when installing , Python takes care of any compilation !!
- Install the following library's numpy,casadi,matplotlib
- Check out the demos in the nmpccodegen-python repo
