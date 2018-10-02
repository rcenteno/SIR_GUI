import config
from loader import*

class VisualizationCanvas(Toplevel):

    def __init__(self, parent, title="Stokes Plots"):

        Toplevel.__init__(self, parent)
        self.__parent = parent
        self.title(title)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+200,
                                  parent.winfo_rooty()+50))
        body = Frame(self)
        self.__body = body
        self.initial_focus = self.__body
        body.pack(padx = 5, pady= 5)
        self.__buttonbox(body)
        self.__canvas(body)
        # enter a local event loop, do not return until the window is destroyed
        self.wait_window(self)
        
        
    # -------------------------------------------------------------------
    def __buttonbox(self, body):
        ''' Add the Close buttons to the canvas.
        '''

        w = Button(body, text="Close", width=10, \
                   command=self.__close)
        w.pack(side=LEFT, padx=5, pady=5)
        
    # -------------------------------------------------------------------

    def __canvas(self, body):

        Nfiles = len(config.legend_names)
        
        # Variables that will contain the data to plot:
        Stokes = []
        Models = []
        Errors = []
        ErrorFileMask=[] # Mask variable for error files
        # Variable that captures if all models contain a z-scale column
        is_z = True
        # ---- Read files in list of files
        for jj in np.arange(0,Nfiles):
            try: # Read Stokes profiles files
                line_ind, wvlen, StkI, StkQ, StkU, StkV = \
                  st.readpro(config.file_path+config.legend_names[jj]+'.per')
                Stokes.append([StkI, StkQ, StkU, StkV])              
            except:
                print('No .per file for ', config.file_path+config.legend_names[jj])
                          
            try: # Read Model files 
                tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray,z, \
                  rho, Pg = st.readmod(config.file_path+config.legend_names[jj]+'.mod')
                Models.append([tau,temp/1e3,Pe,vmic/1e5,B/1e3,vlos/1e5,gamma,phi,\
                                   z/1e3,rho,Pg])
                
                # Check if new model contains a z-scale column. Update is_z.
                is_z = is_z and (np.absolute(z).sum() !=0)
            except:
                print('No .mod file for ', config.file_path+config.legend_names[jj])
                          
            # If the error button is checked, then read error files
            if config.checks['err'].get(): 
                try: # reading error file
                    tau,temp,Pe,vmic,B,vlos,gamma,phi,vmac,ff,stray,z,rho,Pg=\
                      st.readmod(config.file_path+\
                                     config.legend_names[jj]+".err")
                    Errors.append([tau,temp/1e3,Pe,vmic/1e5,B/1e3,vlos/1e5,\
                                    gamma,phi,z,rho,Pg])
                    ErrorFileMask.append(1)
                except: # corresponding error file does not exist
                    ErrorFileMask.append(0)
                    print('No .err file for ', config.file_path+config.legend_names[jj])
                    

        # Calculate default figure limits
        model_array = np.array(Models)
        config.lower_limits = []
        config.upper_limits = []
        for jj in range(0,11):
            #datamin = model_array[:,jj].min()
            #datamax = model_array[:,jj].max()
            if len(model_array) == 0:
                datamin = 0.0
                datamax = 0.0
            else:
                datamin = model_array[:,jj].min()*0.9
                datamax = model_array[:,jj].max()*1.1
            if datamin == datamax:
                datamax = datamin+1
                datamin -= 1
            config.lower_limits.append(datamin)*0.9
            config.upper_limits.append(datamax)*1.1
            
        # Set the toggle to z again, should the user have requested z-scale but not
        # all models have z columns
        if config.checks['toggle'].get()==(u'\u03C4'+'  scale') and not(is_z):
            config.checks['toggle'].set('z scale')

        
        # Number of rows and columns for subplots
        Nrows = int(np.floor(np.sqrt(config.total_chks+1)))
        Ncols = int(np.ceil(float(config.total_chks+1)/Nrows))
        # ---- Create Figure
        plt.close('all')
        sir_fig = plt.figure()
        sir_fig.clear()
        Nplot = 0
        
        # ---- First plot the Stokes parameters
        for k in range(0,4): 
            if config.stokes_chks[k]:
                Nplot = Nplot+1
                axstks = sir_fig.add_subplot(Nrows, Ncols, Nplot)
                axstks.set_title(config.AllStokesTitles[k], \
                                     fontsize=config.figfontsize)

                file_ctr = 0 # Count number of non-existing Stokes files,
                # so that the filename index jj is consistent for Stokes
                # variable (could have fewer Stokes files than model files)
                
                # ---- Loop through different profile files:
                for jj in np.arange(0,Nfiles): 
                    if config.per_mask[jj]:
                        axstks.plot(Stokes[jj-file_ctr][k], \
                                        color = config.colorlist[jj], \
                                        label=config.legend_names[jj],\
                                        linewidth=0.9)
                        axstks.set_xlabel(r'$\Delta\lambda$(Arb. units)',\
                                              fontsize='small')
                        axstks.tick_params(axis='both', labelsize='small')
                        #if sys.version_info[0] < 3:
                        #   plt.locator_params(axis='both', nbins=5)

                    else:
                        file_ctr = file_ctr + 1
                handles1, labels1 = axstks.get_legend_handles_labels()

                        
        # ---- Now plot the atmospheric model parameters                    
        for k in range(0,7): # Model parameters
            if config.model_chks[k]:
                Nplot = Nplot+1
                axstks = sir_fig.add_subplot(Nrows, Ncols, Nplot)
                axstks.set_title(config.AllModelTitles[k], \
                                     fontsize=config.figfontsize)
                file_ctr = 0

                # ---- Loop through different model files:
                for jj in np.arange(0,Nfiles):
                    if config.mod_mask[jj]: # Model file exists, plot model

                        # Plot in z-scale, if column exists and toggle says so
                        if (config.checks['toggle'].get() == (u'\u03C4'+'  scale')):
                            
                            # plot with errorbars:
                            if config.checks['err'].get() and ErrorFileMask[jj]:
                                # Some .mod files might not have associated .err files 
                                tot_err_files = np.sum(np.array(ErrorFileMask[:jj]))
                                # number of missing error files
                                missing = int(jj - tot_err_files) 
                                axstks.errorbar(Models[jj-file_ctr][8], \
                                                    #Models[jj][k+1], \
                                                    Models[jj-file_ctr][k+1], \
                                                    yerr=Errors[jj-file_ctr-missing][k+1],\
                                                    label=config.legend_names[jj],\
                                                    color = config.colorlist[jj],\
                                                    fmt='-',linewidth=0.7)
                                axstks.set_xlabel('z (Mm)',fontsize='small')

                            else: #plot without errors
                                axstks.plot(Models[jj-file_ctr][8], \
                                                Models[jj-file_ctr][k+1], \
                                                label=config.legend_names[jj],\
                                                color = config.colorlist[jj], \
                                                linewidth=0.9)
                                axstks.set_xlabel('z (Mm)',fontsize='small')
                 
                            plt.axis([config.lower_limits[8],\
                                          config.upper_limits[8],\
                                          config.lower_limits[k+1],\
                                          config.upper_limits[k+1]])      

                        else: # Plot in tau-scale (because user request through
                            # toggle or because z column does not exist)
                            # plot with errorbars:

                            if config.checks['err'].get() and ErrorFileMask[jj]:
                                # Some .mod files might not have associated .err files 
                                tot_err_files = np.sum(np.array(ErrorFileMask[:jj]))
                                # Number of missing error files
                                missing = int(jj - tot_err_files)
                                axstks.errorbar(Models[jj-file_ctr][0], \
                                                    #Models[jj][k+1], \
                                                    Models[jj-file_ctr][k+1], \
                                                    yerr=Errors[jj-file_ctr-missing][k+1],\
                                                    label=config.legend_names[jj],\
                                                    color = config.colorlist[jj],\
                                                    fmt='-',linewidth=0.7)
                                axstks.set_xlabel(r'log($\tau$)',\
                                                        fontsize='small')
                                        
                            else: #plot without errors
                                axstks.plot(Models[jj-file_ctr][0], \
                                                Models[jj-file_ctr][k+1], \
                                                label=config.legend_names[jj],\
                                                color = config.colorlist[jj], \
                                                linewidth=0.9)
                                axstks.set_xlabel(r'log($\tau$)',\
                                                      fontsize='small')
                         
                            plt.axis([config.lower_limits[0],\
                                          config.upper_limits[0],\
                                          config.lower_limits[k+1],\
                                          config.upper_limits[k+1]])
                        axstks.tick_params(axis='both', labelsize='small')

                        if sys.version_info[0] < 3:
                            plt.locator_params(axis='both', nbins=5)
                        
                    else:
                        file_ctr = file_ctr + 1

        handles, labels = axstks.get_legend_handles_labels()
      
        # Unify unique handles and lables from the Stokes and Model plots:
        ind_counter = 0
        for label in labels1:
            if label in labels:
                ind_counter += 1
            else:
                labels.append(label)
                handles.append(handles1[ind_counter])
                ind_counter += 1

        plt.tight_layout()
        # make the legend
        plt.figlegend(handles, labels, bbox_to_anchor=[0.95, 0.2],\
                          loc = 'lower right', ncol=1, \
                          labelspacing=0.1,fontsize=8 )

        canvas = FigureCanvasTkAgg(sir_fig, self)

        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, \
                                    expand=True)
        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar = NavigationToolbar2Tk(canvas, self)

        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    

    def __close(self, event=None):
        ''' Method that handles the window closing.
        '''

        # put focus back to the parent window
        plt.close('all')
        self.__parent.focus_set()
        self.destroy()

