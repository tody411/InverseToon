
Inverse Toon Shading (Python) {#mainpage}
====

Simple Python demos of Inverse Toon Shading [Xu et al. 2015].

Their main idea is using **isophote**, a contour of equal luminance.
I would like to test each step of normal estimation process based on the **isophote** concept.

1. Well-defined normals
    - Intersecting isophotes
2. Isophote normals
    - 2D arc-length interpolation
    - Integrating 2D tangent direction
    - 3D projection
3. Full normal field
    - Diffuse isophote normals
    - Project back to isophote constraint

## Result
*Status*: Under construction.

## Installation

*Note*: This program was only tested on **Windows** with **Python2.7**.
**Linux** and **Mac OS** are not officially supported,
but the following instructions might be helpful for installing on those environments.

### Dependencies
Please install the following required python modules.

* **NumPy**
* **SciPy**
* **matplotlib**
* **OpenCV**
* **PyAMG**

As these modules are heavily dependent on NumPy modules, please install appropriate packages for your development environment (Python versions, 32-bit or 64bit).
For 64-bit Windows, you can download the binaries from [**Unofficial Windows Binaries for Python Extension Packages**](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

This program also uses **docopt** for CLI.
**docopt** will be installed automatically through the following **pip** command for main modules.

### Install main modules
*Status*: Under construction.

<!-- You can use **pip** command for installing main modules.
Please run the following command from the shell.

``` bash
  > pip install git+https://github.com/tody411/InverseToon.git
``` -->

## Usage
*Status*: Under construction.

## Future tasks

* [ ] Complete implementation.
* [ ] Update result section.
* [ ] Provide API document.

## License

The MIT License 2015 (c) tody