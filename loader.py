#python3.7 -m pip install scipy
# Imports
import sys
import os
import glob

import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import matplotlib.pyplot as plt


if sys.version_info[0] < 3:
    # for Python2
    from ttk import *
    from Tkinter import *
    import tkFont
    #import cPickle as pickle
    import tkMessageBox, tkFileDialog
else:
    # for Python3
    from tkinter.ttk import *
    from tkinter import *
    import tkinter.font as tkFont
    #import pickle as pickle
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    from matplotlib import style
    style.use("ggplot")


import sirtools2 as st
