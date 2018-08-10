"""
Author: R. Centeno
Date: 2018-07-27

GUI that allows user to visualize output (Stokes profiles and model atmospheres)
from the SIR inversion code.

Uses 4 files:
    loader.py: loads all necessary modules
    config.py: contains some global variables
    visualization.py: defines VisualizationCanvas class with canvas and figures
    sirgui.py (this file): Main program. Calls SirGUI class, which contains 
        the menu and main functionality of the GUI.
Third party imports: 
    numpy
    matplotlib
    sirtools2

Updates:

- 2018/09/08:
    ** Changed model_chks and stokes_chks to be global variables. They are now checked in 
       __plot_stokes before plotting. If nothing is checked, the canvas class is not called.
    ** Corrected a bug in visualization.py: file_ctr was not being subtracted from model 
       jj index to account for model files that were not being read. The wrong model was being
       plotted when there were more .per files than .mod files in the user selection.
    ** Introduced and error file counter (missing) in visualization.py to account for 
       missing .err files. 
"""


import config # file with global variables
from loader import * #file with imports
from visualization import *

class SirGUI:

    def __init__(self, master):
        # Initialize class. Set some attributes. Call main menu method.

        self.__master = master
        self.__main_frame = Frame(master)
        self.__toggletext = StringVar() # toggle button for height scale
        self.__toggletext.set('z scale')
        config.checks['toggle']=self.__toggletext
        self.__main_menu(self.__main_frame) # main menu, contains all buttons.
        self.__main_frame.grid()
        
    def __changeheightscale(self):
        # Method that changes the global variable and class attribute for the
        # toggle button that allows the user to switch between z and tau heigh scales.
        if self.__toggletext.get()== 'z scale':
            self.__toggletext.set(u'\u03C4'+'  scale')
        else:
            self.__toggletext.set('z scale')
        config.checks['toggle']=self.__toggletext
        
    def __main_menu(self, main_frame):
        # Mehod that defines the file dialog, as well as the check buttons and
        # buttons for the user to interact with the GUI
        
        # ---- File Selection Button - Calls: __file_select()
        b = Button(main_frame, text="Select File", width=25,\
                       command=self.__file_select, pady=20, padx=20)
        b.grid(columnspan=3, sticky=(W+E), padx=10)
        
        # ---- Stokes Check Buttons:
        # All the values of all the check buttons are saved in a global dictionary
        # called "checks", which is defined in config.py
        
        stklabel = Label(main_frame, text="Select Stokes profiles to plot:",\
                             padx =15, pady=10)
        stklabel.grid(columnspan=3, sticky=(W))

        chk_state_I = BooleanVar()
        chk_state_I.set(True)
        Ichk = Checkbutton(main_frame, text="Stokes I", \
                               variable = chk_state_I, padx =10)
        Ichk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['I'] = chk_state_I
        
        chk_state_Q = BooleanVar()
        chk_state_Q.set(True)
        Qchk = Checkbutton(main_frame, text="Stokes Q", \
                               variable = chk_state_Q, padx =10)
        Qchk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['Q'] = chk_state_Q
        
        chk_state_U= BooleanVar()
        chk_state_U.set(True)
        Uchk = Checkbutton(main_frame, text="Stokes U", \
                               variable = chk_state_U, padx =10)
        Uchk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['U'] = chk_state_U
                
        chk_state_V= BooleanVar()
        chk_state_V.set(True)
        Vchk = Checkbutton(main_frame, text="Stokes V",\
                               variable = chk_state_V, padx =10)
        Vchk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['V'] = chk_state_V

        # ---- Model Check Buttons
        
        ModelLabel = Label(main_frame, \
                               text="Select Model variables to plot:", \
                               padx =20, pady=20)
        ModelLabel.grid(columnspan=3, sticky=(W))

        chk_state_temp = BooleanVar()
        chk_state_temp.set(True)
        TempChk = Checkbutton(main_frame, text="Temmperature", \
                              variable = chk_state_temp, padx =10)
        TempChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['T'] = chk_state_temp


        chk_state_pe = BooleanVar()
        chk_state_pe.set(False)
        PeChk = Checkbutton(main_frame, text="Electron Pressure", \
                            variable = chk_state_pe, padx =10)
        PeChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['Pe'] = chk_state_pe

        chk_state_vmic = BooleanVar()
        chk_state_vmic.set(False)
        vmicChk = Checkbutton(main_frame, text="Microturbulence", \
                                variable = chk_state_vmic, padx =10)
        vmicChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['vmic'] = chk_state_vmic

        chk_state_B = BooleanVar()
        chk_state_B.set(True)
        BChk = Checkbutton(main_frame, text="Magnetic field ", \
                           variable = chk_state_B, padx =10)
        BChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['B'] = chk_state_B
             

        chk_state_vlos = BooleanVar()
        chk_state_vlos.set(True)
        vlosChk = Checkbutton(main_frame, text="LOS velocity", \
                                variable = chk_state_vlos, padx =10)
        vlosChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['vlos'] = chk_state_vlos
                        

        chk_state_gamma = BooleanVar()
        chk_state_gamma.set(True)
        gammaChk = Checkbutton(main_frame, text="Inclination", \
                                variable = chk_state_gamma, padx =10)
        gammaChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['gamma'] = chk_state_gamma
                        
        chk_state_phi = BooleanVar()
        chk_state_phi.set(True)
        phiChk = Checkbutton(main_frame, text="Azimuth", \
                                variable = chk_state_phi, padx =10)
        phiChk.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['phi'] = chk_state_phi
                                
        # ---- Error Check Button
        
        err_check = BooleanVar()
        err_check.set(0)
        ErrorButton = Checkbutton(main_frame, text = 'Plot Errors', \
                                    variable = err_check, padx = 20, pady = 10)
        ErrorButton.grid(columnspan=3, sticky=(W), padx =20)
        config.checks['err'] = err_check

   
        # ---- Plot, z/tau scale, Close Buttons

        # Plot Button - Calls: __plot_stokes
        b = Button(main_frame, text="Plot", width=8,\
                       command=self.__plot_stokes, pady=10, padx=5)
        b.grid(row=50,column=0)
        
        # Height scale toggle button - Calls __change_scale_height
        togglebutton = Button(main_frame, width=8, command= self.__changeheightscale, \
                                  textvariable = self.__toggletext,\
                                  padx=5, pady=10)
        togglebutton.grid(row=50,column=1)

        # Close button - Calls: Quit
        b = Button(main_frame, text="Close", width=8, command=quit, \
                       pady=10, padx=5)
        b.grid(row=50, column=2)

    def __file_parse(self, filelist):
        # Method that parses the general file list, creates all the figure
        # legend names and the masks that define whether a given profile or model
        # file exists or not (the user can select more models than profiles, or
        # vice-versa, or may select models and profiles that don't have
        # correspondence to each other).
        
        per_files = [x for x in filelist if x.endswith('.per')]
        mod_files = [x for x in filelist if x.endswith('.mod')]

        per_names = [] # temporary var that saves profile (.per) files
        mod_names = [] # temporary var that saves model (.mod) files
        
        try: #for Python 3
            config.per_mask.clear()
            config.mod_mask.clear()
        except: # for python 2.7
            config.per_mask[:] = []
            config.mod_mask[:] = []

        # Get file names without path or extension. Will use them for
        # figure legends
        for file in per_files:
            per_names.append(file[:-4].rpartition('/')[2])
        for file in mod_files:
            mod_names.append(file[:-4].rpartition('/')[2])
        # Save the file path (common to all files)
        config.file_path = file.rpartition('/')[0]+'/'

        
        if per_names != mod_names: # Profile and model lists are different
            # keep all unique names
            config.legend_names = list(set(per_names+mod_names))
            # create masks for profiles and models
            for name in config.legend_names:
                if name in per_names:
                    config.per_mask.append(1)
                else:
                    config.per_mask.append(0)
                    
            for name in config.legend_names:
                if name in mod_names:
                    config.mod_mask.append(1)
                else:
                    config.mod_mask.append(0)
                  
        else: # Both lists are identical
            config.legend_names = mod_names
            config.per_mask = [1]*len(mod_names)
            config.mod_mask = [1]*len(mod_names)

        
    def __file_select(self):
        # Method that opens a system file dialog and saves files selected by user.
        # Calls self.__file_parse to separate mod and per files and creates masks.
        filez = tkFileDialog.askopenfilenames\
          (initialdir='./', title="Select a file:", \
               filetypes=[('SIR files','*.per *.mod')])
        #filez = tkFileDialog.askopenfilenames\
        #  (initialdir='./', title="Select a Stokes file:",\
        #       filetypes=(('Stokes files','*.per'),('Model files', '*.mod')))
        filelist = list(filez)
        config.filenames = filelist

        if filez:
            self.__file_parse(filelist)
        else:
            tkMessageBox.showwarning("No file selected","Plese load a file")
        
    def __plot_stokes(self):
        # Method that calls the VisualizationCanvas class, that does all the
        # plots and creates the canvas

        config.stokes_chks = np.array([int(config.checks['I'].get()),\
                                    int(config.checks['Q'].get()),\
                                    int(config.checks['U'].get()),\
                                    int(config.checks['V'].get())])
        config.model_chks = np.array([int(config.checks['T'].get()),\
                                   int(config.checks['Pe'].get()),\
                                   int(config.checks['vmic'].get()),\
                                   int(config.checks['B'].get()),\
                                   int(config.checks['vlos'].get()),\
                                   int(config.checks['gamma'].get()),\
                                   int(config.checks['phi'].get())])
        # number of Stokes and Models Checked                           

        config.n_stokes_chks = np.sum(config.stokes_chks)      
        config.n_model_chks = np.sum(config.model_chks)
        # Total number of subplots plus 1 (for figure legend)
        config.total_chks = config.n_stokes_chks + config.n_model_chks

        if config.total_chks > 0:
            canvas = VisualizationCanvas(self.__main_frame, title = "Stokes Plots")
        else:
            tkMessageBox.showwarning("No parameters to plot","Plese check one or more parameters to plot")
#########################################################################
#########################################################################
#########################################################################


root = Tk()
root.wm_title('SIR GUI')

sirgui = SirGUI(root)
root.mainloop()
        
