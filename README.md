# SIR_GUI
Python GUI to display atmospheric models and Stokes profiles from the SIR spectral line inversion code (which you can find in https://github.com/BasilioRuiz/SIR-code).
This is a Python "translation" of the IDL visualization package graphics2.pro that comes with the SIR distribution.

Running the GUI:
> python sirgui.py

Author:
Rebecca Centeno,
High Altitude Observatory (NCAR)

Date: August 10, 2018

Contains:
- sirtools2.py: module with routines to read and write SIR formatted input and output spectral profiles and atmospheric models.
- config.py: global variables for GUI
- loader.py: Calls imports for GUI
- visualization.py: Defines canvas class for GUI to generate figures
- sirgui.py: GUI root

Third party modules needed:
- numpy
- matplotlib

