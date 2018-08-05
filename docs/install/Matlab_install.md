# Installation of nmpccodegen on Matlab

## What do I need?
- GNU toolchain with make (more info [here](Toolchain_install.md))
- Matlab with casadi 3.2.x or higher
- Cmake

## !!! Make sure python and the toolchain are either BOTH 32 or BOTH 64 bit !!

## How to install
- make sure Cmake,make and gcc are installed (run Matlab_test_utils.m to test if they are available)
- git clone the repo 
- add src_matlab to your matlab path
- !! no compilation is required when installing , Matlab takes care of any compilation !!
- install the following library's [casadi](http://casadi.org), No toolboxes are required 
- Check out demos/Matlab in the nmpccodegen repo

