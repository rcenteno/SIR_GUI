""" 
July 2018
Rebecca Centeno

This module contains routines to write and read SIR input and output.
The reading routines are used by the visualization GUI: SirGUI

******* Uses:

>> numpy

******* Contains:

>> line_ind, wvlen, StkI, StkQ, StkU, StkV = readpro(filename)

>> tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z, rho, Pg  = readmod(filename)

>>  writepro(filename, line_ind, wvlen, StkI, StkQ, StkU, StkV)

>> writemod(filename, tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z=z, rho=rho, Pg = Pg)

******* Changes:

10-01-2018: Change in readpro so that line index is not assumed to be an integer.

"""

def readpro(filename):

    """ 
    Reads a line profile from a .per file
    Call:
    line_ind, wvlen, StkI, StkQ, StkU, StkV = st.readpro(filename)
    """
    
    from numpy import array

    f = open(filename, 'r')

    line_ind = []
    wvlen = []
    StkI = []
    StkQ = []
    StkU = []
    StkV = []
    
    for line in f:
        data = line.split()
        line_ind.append(float(data[0]))
        wvlen.append(float(data[1]))
        StkI.append(float(data[2]))
        StkQ.append(float(data[3]))
        StkU.append(float(data[4]))
        StkV.append(float(data[5]))

    f.close()

    line_ind = array(line_ind)
    wvlen = array(wvlen)
    StkI = array(StkI)
    StkQ = array(StkQ)
    StkU = array(StkU)
    StkV = array(StkV)

    return(line_ind, wvlen, StkI, StkQ, StkU, StkV)

def readmod(filename):

    """ 
    Reads SIR model file with 8 or 11 columns.
    Call:
    tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z, rho, Pg  = readmod(filename)
    """

    from numpy import array
    
    f = open(filename)
    # Read the first line which contains vmac, filling factor, stray light
    firstline = f.readline()
    vmac, ff, stray = firstline.split()

    vmac = float(vmac)
    ff = float(ff)
    stray = float(stray)
    
    # the rest of the file is 8 or 11 columns, with:
    # tau, temperature, electron pressure, microturbulent velocity
    # field strength, LOS velocity, inclination, azimuth
    # and 3 optional columns:
    # z scale, density, gas pressure
   
    tau = []
    temp = []
    Pe = []
    vmic = []
    B = []
    vlos =[]
    gamma =[]
    phi = []
    z = []
    rho = []
    Pg = []
 
    
    for line in f:
        data = line.split()
        ncol = len(data)
        tau.append(float(data[0]))
        temp.append(float(data[1]))
        Pe.append(float(data[2]))
        vmic.append(float(data[3]))
        B.append(float(data[4]))
        vlos.append(float(data[5]))
        gamma.append(float(data[6]))
        phi.append(float(data[7]))
        
        if ncol == 11:
            z.append(float(data[8]))
            rho.append(float(data[9]))
            Pg.append(float(data[10]))
        else:
            z.append(0.)
            rho.append(0.)
            Pg.append(0.)
    f.close()
    
        #convert to array
    tau = array(tau)
    temp = array(temp)
    Pe = array(Pe)
    vmic = array(vmic)
    B = array(B)
    vlos = array(vlos)
    gamma = array(gamma)
    phi = array(phi)

    z = array(z)
    rho = array(rho)
    Pg = array(Pg)

    return(tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z, rho, Pg)

def writepro(filename, line_ind, wvlen, StkI, StkQ, StkU, StkV):
    """ 
    Routine that writes the Stokes profiles into a SIR formatted Stokes file.
    Call:
    writepro(filename, line_ind, wvlen, StkI, StkQ, StkU, StkV)
    """

    f = open(filename, "w+")

    for k in range(0, len(line_ind)):
        f.write('     {0}   {1:> 10.4f}  {2:> 8.6e} {3:> 8.6e} {4:> 8.6e} {5:> 8.6e} \n'.format(line_ind[k], wvlen[k], StkI[k], StkQ[k], StkU[k], StkV[k]))

    f.close()

    return()

def writemod(filename, tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z=None, rho=None, Pg=None):

    """  
    Routine that writes the atmospheric model files in SIR format.
    Call:
    writemod(filename, tau, temp, Pe, vmic, B, vlos, gamma, phi, vmac, ff, stray, z=z, rho=rho, Pg = Pg)
    """

    f = open(filename, "w+")
    f.write('  {0:> 10.8f}      {1:> 10.8f}      {2:> 10.8f} \n'.format(vmac, ff, stray))

    if z is None:
        for k in range(0, len(tau)):
            f.write(' {0:> 7.4f}  {1:> 6.1f} {2:> 8.5E} {3:> 5.3E} {4:> 6.4E} {5:> 6.4E} {6:> 6.4E} {7:> 6.4E} \n'.format(tau[k], temp[k], Pe[k], vmic[k], B[k], vlos[k], gamma[k], phi[k]))

    else:
        if z is not None and Pg is not None and rho is not None:
            for k in range(0, len(tau)):
                f.write(' {0:> 7.4f}  {1:> 6.1f} {2:> 8.5E} {3:> 5.3E} {4:> 6.4E} {5:> 6.4E} {6:> 6.4E} {7:> 6.4E} {8:> 6.4E} {9:> 6.4E} {10:> 6.4E} \n'.format(tau[k], temp[k], Pe[k], vmic[k], B[k], vlos[k], gamma[k], phi[k], z[k], rho[k], Pg[k]))

    
    f.close()

    return()
