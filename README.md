# VESIcal
A generalized python library for calculating and plotting various things related to mixed volatile (H2O-CO2) solubility in silicate melts.

## Installation

First, obtain Python3.x and pandas if you do not already have them. VESIcal can be installed with one line. Open a terminal and type the following:

.. code-block::

    pip install VESIcal

Check that the installation worked by entering the following lines into a terminal:

.. code-block::

   python
   import VESIcal as v

If no output is returned, VESIcal has installed properly! You will very likely, however, see a warning telling you that no module named 'thermoengine' could be found. The installation you performed via pip attempts to install all dependencies (other libraries that VESIcal requires), but thermoengine is not available via pip and so must be manually installed.

Dependencies that should automatically be installed for you are:

   - pandas
   - numpy
   - matplotlib
   - cycler
   - abc
   - scipy
   - sys
   - sympy
   - copy

If any warnings related to these libraries appear, try installing them as you did VESIcal: with 'pip install [package]'.

thermoengine is the ENKI implementation of MELTS (MagmaSat), which is the backbone of the entire VESIcal library. VESIcal cannot be run without thermoengine at this time, however a VESIcal-lite that does not include MagmaSat is planned. To install thermoengine, please refer to the ENKI documentation here: `https://gitlab.com/ENKI-portal/ThermoEngine <https://gitlab.com/ENKI-portal/ThermoEngine>`_.
