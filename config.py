from loader import *
    
AllStokesTitles =["Stokes I", "Stokes Q", "Stokes U", "Stokes V"]
AllModelTitles = ["Temperature (kK)", r"Pe (dyn cm$^{-2}$)", \
                      "Microturbulence (km/s)","B (kG)", \
                      "Vlos (km/s)", r"Inclination ($^{\circ}$)", \
                      r"Azimuth ($^{\circ}$)"]
colorlist = ["teal","sandybrown", "darkorchid","red", "blue",\
                 "purple","yellow", "pink", "black","green","sienna"]

filenames=[]
checks = {}
legend_names = []
per_mask = []
mod_mask = []
lower_limits = []
upper_limits = []
file_path = ''

stokes_chks=[]
model_chks=[]
n_stokes_chks = 0.
n_model_chks = 0.
total_chks = 0.

figfontsize = 8
