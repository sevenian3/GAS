# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:09:02 2019

@author: 
"""

#
#
#his module can serve as the main method
#
#

#plotting:
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
import math
import numpy
#from scipy.linalg.blas import daxpy
#from scipy.linalg.blas import ddot
#from scipy.linalg.blas import dscal
#from scipy.linalg.blas import idamax

"""
from Documents.ChromaStarPy.GAS.blas.Daxpy import daxpy
from Documents.ChromaStarPy.GAS.blas.Ddot import ddot
from Documents.ChromaStarPy.GAS.blas.Dscal import dscal
from Documents.ChromaStarPy.GAS.blas.Idamax import idamax

from Documents.ChromaStarPy.GAS.linpack.Dgesl import dgesl
from Documents.ChromaStarPy.GAS.linpack.Dgefa import dgefa
"""

from functools import reduce
import subprocess
import os
import sys


import BlockData
#import GsRead
import GsRead2
import GsTabl
import GasEst
import Gas

"""
import Documents.ChromaStarPy.GAS.BlockData
#from Documents.ChromaStarPy.GAS.GsRead import gsread
#from Documents.ChromaStarPy.GAS.GasEst import gasest
#from Documents.ChromaStarPy.GAS.Gas import gas
import Documents.ChromaStarPy.GAS.GsRead
import Documents.ChromaStarPy.GAS.GasEst
import Documents.ChromaStarPy.GAS.Gas
"""
#############################################
#
#
#
#    Initial set-up:
#     - import all python modules
#     - set input parameters 
#     
#
#
##############################################

#Detect python version
pythonV = sys.version_info
if pythonV[0] != 3:
    print("")
    print("")
    print(" ********************************************* ")
    print("")
    print("WARNING!!  WARNING!!   WARNING!!")
    print("")
    print("")
    print("ChromaStarPy/GAS developed for python V. 3!!" )
    print("")
    print("May not work in other version")
    print("")
    print("")
    print("*********************************************** ")
    print("")
    print("")



thisOS = "unknown" #default
myOS= ""
#returns 'posix' form unix-like OSes and 'nt' for Windows??
thisOS = os.name
print("")
print("Running on OS: ", thisOS)
print("")

absPath0 = "./"  #default

if thisOS == "nt":
    #windows
    absPath0 = subprocess.check_output("cd", shell=True)
    backSpace = 2
elif thisOS == "posix":
    absPath0 = subprocess.check_output("pwd", shell=True)
    backSpace = 1

absPath0 = bytes.decode(absPath0)

#remove OS_dependent trailing characters 'r\n'
nCharsPath = len(absPath0)
nCharsPath -= backSpace
absPath0 = absPath0[0: nCharsPath]

slashIndex = absPath0.find('\\') #The first backslash is the escape character!
while slashIndex != -1:
    #python strings are immutable:
    absPathCopy = absPath0[0: slashIndex]
    absPathCopy += '/'
    absPathCopy += absPath0[slashIndex+1: len(absPath0)]
    absPath0 = absPathCopy
    #print(absPathCopy, absPath0)
    slashIndex = absPath0.find('\\')

absPath = absPath0 + '/'

##makePlot = Input.makePlot
#makePlot = "yes"
#print("")
#print("Will make plot: ", makePlot)
#print("")
#stop
#color platte for plt plotting
#palette = ['black', 'brown','red','orange','yellow','green','blue','indigo','violet']
#grayscale
#stop
#Grayscale:
numPal = 12
palette = ['0.0' for i in range(numPal)]
delPal = 0.04
#for i in range(numPal):
#    ii = float(i)
#    helpPal = 0.481 - ii*delPal
#    palette[i] = str(helpPal) 

palette = [ str( 0.481 - float(i)*delPal ) for i in range(numPal) ]
numClrs = len(palette)


#General file for printing ad hoc quantities
#dbgHandle = open("debug.out", 'w')
outPath = absPath + "/Outputs/"

#fileStem = Input.fileStem
fileStem = "GsCalc"

#Set input pressure and isolv here for file naming:
pt = 1.0e5
isolv = 1

fileStem = fileStem + ".Read2." + "pt" + str(int(math.log10(pt))).strip() + "is" + str(isolv)
outFileString = outPath+fileStem+".out"  #Report for humans
outFileString2 = outPath+fileStem+".2.out" #PPs for plotting
print(" ")
print("Writing to files ", outFileString)
print(" ")
outFile = open(outFileString, "w")
outFile2 = open(outFileString2, "w")

#program gcalc

"""
#The seven universal FORTRAN "commons"
common /consts/ pi,sbcon,kbol,cvel,gcon,hpl,hmass,t0,everg
common /gasp/ name,ip,comp,awt,nspec,natom,itab,ntab,indx,
     #    iprint,gsinit,print0
common /gasp2/ ipr,nch,nel,ntot,nat,zat,neut,idel,indsp,
     #    indzat,iat,natsp,iatsp
common /lin/ nlin1,lin1,linv1,nlin2,lin2,linv2
common /equil/ logk,logwt,it,kt,type
common /opacty/ chix,nix,nopac,ixa,ixn,opinit,opflag,opchar,iopt
common /stellr/ mstar,lstar,rstar,ms,ls,rs,teff,logg,mbol,comt
"""

#Try this:
#global pi, sbcon, kbol, cvel, gcon, hpl, hmass, t0, everg # /consts/
global kbol, hmass, t0 # /consts/
global name, ip, comp, awt, nspec, natom, itab, ntab, indx, iprint, gsinit, print0 #/gasp/
global ipr, nch, nel, ntot, nat, zat, neut, idel, indsp, indzat, iat, natsp, iatsp #/gasp2/
global nlin1, lin1, linv1, nlin2, lin2, linv2 #/lin/
global logk, logwt, it, kt, type0 #equil
#global chix, nix, nopac, ixa, ixn, opinit, opflag, opchar, iopt #/opacty/
global chix, nix, ixa, ixn #/opacty/
#global mstar, lstar, rstar, ms, ls, rs, teff, logg, mbol, comt #/stellr/

outString = ""

print0 = False

p0 = [0.0e0 for i in range(40)]
pp = [0.0e0 for i in range(150)]
p = [0.0e0 for i in range(40)]
ppix = [0.0e0 for i in range(30)]
a = [0.0e0 for i in range(625)]

#c cis:
     
fp = [0.0e0 for i in range(150)]
#name = [0.0e0 for i in range(150)]
#ip = [0.0e0 for i in range(150)]
#comp = [0.0e0 for i in range(40)]
#awt = [0.0e0 for i in range(150)]

#itab = [0 for i in range(83)]
#ntab = [0 for i in range(5)]
#indx = [ [ [ [ [0 for i in range(2)] for j in range(5) ] for k in range(7) ] for l in range(26) ] for m in range(4) ]

#common /gasp/ name,ip,comp,awt,nspec,natom,gsinit,itab,ntab,indx

#BlockData.block_data()

#print("Calling GsRead:")
#GsRead.gsread(outFile)
GsRead2.gsread(outFile)
#GsTabl.gstabl()  #necessary??

#nspec = GsRead.nspec
#name = GsRead.name
nspec = GsRead2.nspec
name = GsRead2.name
#print("GsCalc: nspec: ", nspec)
outString = ""
for k in range(nspec):
    outString = outString + " " + name[k]
outString+="\n"
outFile2.write(outString)


# Input parameters are now command line arguments

#c      call time(1,0,mscpu)
#c      cpu1=mscpu/1000.0
#c      write(7,100)
#      write(6,100)
#  100 format('enter: t ,p, and pe')
#c      call fread(5,'3r*8:',t,pt,pe0)
#      read(5, *) t, pt, pe0
#c      write(7,150)
 #     write(6,150)
# 150 format('enter: tolerance, max # iter. and isolv')
#c      call fread(5,'r*8,2i:',tol,maxit,isolv)
#      read(5, *) tol, maxit, isolv
 
#Get and parse the command line arguments:
# sys.argv[0] is the name of the script
 
"""
t = float(sys.argv[1])
pt = float(sys.argv[2])
pe0 = float(sys.argv[3])
tol = float(sys.argv[4])
maxit = int(sys.argv[5])
isolv = int(sys.argv[6])

print("t ", t, " pt ", pt, " pe0 ", pe0, " tol ", tol, " maxit ", maxit, " isolv ", isolv)
"""

#For now:
#t = 6000.0
t1 = 1500.0
t2 = 6500.0
dt = 100.0
# Set this above: pt = 100000.0
#pe0 = 100.0
tol = 1.0e-4
maxit = 100
# Set this above: isolv = 1

nt = (t2 - t1) / dt + 1
nt = int(nt)
pe0 = 0.01 * pt

outString = ("%4s %12.3e\n" %("PT ", pt))
outFile.write(outString)
outFile2.write(outString)

outStringHead = ("%11s %8s %5s %4s %4s %8s\n"\
             %("t ", " rholog ", " gmu ", " fd ", " fe ", " fp(k) "))
outFile2.write(outStringHead)     
#testing:
#tol = 1.0e-1
#maxit = 1

original = sys.stdout
#sys.stdout = open('./redirect.txt', 'w')

for k in range(nt):
    
    k = float(k)
    t = t1 + dt*k
    
    #Try making return value a tuple:
    #print("Before GasEst pe0 ", pe0)
    #gasestReturn = GasEst.gasest(isolv, t, pt, pe0)
    gasestReturn = GasEst.gasest(isolv, t, pt)
    pe0 = gasestReturn[0]
    p0 = gasestReturn[1]
    neq = gasestReturn[2]

#print("GsCalc: pe0 ", pe0, " p0 ", p0, " neq ", neq)

    #print("Before gas pe0 ", pe0)
    gasReturn = Gas.gas(isolv, t, pt, pe0, p0, neq, tol, maxit, outFile)
    a = gasReturn[0]
    nit = gasReturn[1]
    pe = gasReturn[2]
    pd = gasReturn[3]
    pp = gasReturn[4]
    ppix = gasReturn[5]
    gmu = gasReturn[6]
    rho = gasReturn[7]
    

#print("GsCalc: rho ", rho)
#print("GsCalc: gmu ", gmu)

    rholog= math.log10(rho)
    fd= -99.0e0
    if(pd/pt > 0.0e0):
        fd = math.log10(pd/pt)
    fe= -99.0e0
    if(pe/pt > 0.0e0): 
        fe = math.log10(pe/pt)

    for n in range(nspec):
        fp[n]= -99.0e0
        if (pp[n]/pt > 0.0e0):
            fp[n]= math.log10( pp[n]/pt)

    #c      write(7,200) t,rholog,gmu,fd,fe,(fp(k),k=1,nspec)
        
    #print("t ", t, " pt ", pt, " rholog ", rholog, " gmu ", gmu, " fd ", fd, " fe ",fe)

    #print("pp, fp:")
    #for k in range(nspec):
    #    print("k ", k, pp[k], fp[k])
    #  200 format(1x,f10.2,160f10.5)
    outFile.write(outStringHead)
    outString = ("%11.2f %10.5f %10.5f %10.5f %10.5f\n"\
                 %(t, rholog, gmu, fd, fe))
    outFile.write(outString)
    outFile2.write(outString)
    
    outString = ""    
    for j in range(nspec):
        outString = outString + " " + str(fp[j])
    outString+="\n"
    outFile.write(outString)
    outFile2.write(outString)

#sys.stdout = original
outFile.close()
outFile2.close()
