# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:49:59 2019

@author: IanShort
"""

#REads in output from GsCalc and prepares plots similar to those of 
#Phil Bennet's M.Sc. thesis

#Ian Short
#Saint Mary's University

#June 2019

#
#
#his module can serve as the main method
#
#

#plotting:
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
import pylab

import math
import numpy

from functools import reduce
import subprocess
import os
import sys

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
dataPath = absPath + "/Outputs/"

#fileStem = "GsCalc.Diatom.pt5is1.2"
#colorCode = 'red'
fileStem = "GsCalc.Read2.pt5is1.2"
colorCode = 'black'
#fileStem = "GsCalc.Test.pt5is1.2"
#colorCode = 'green'
#fileStem = "GsCalcpt5is1.2"
#colorCode = 'red'
#fileStem = "fort.7"
#colorCode = 'red'

inFileString = dataPath+fileStem+".out"  #Report for humans
print(" ")
print("Reading from file ", inFileString)
print(" ")
#inFile = open(inFileString, "w")

whichSpecies = "OH"

name = []
fp = []
pp = []
t = []
rholog = []
gmu = []
fd = []
fe = []

nspec = 0
inLine1 = ""
inLine2 = ""
#fields = [" " for i in range(2)] 

#Initialize block accumulator:
numTemp = -1

#with open("", 'r', encoding='utf-8') as inputHandle:
with open(inFileString, 'r') as inputHandle:
    
    #1st line is list of species names separated by white space
    inLine1 = inputHandle.readline()
    name = inLine1.split()
    nspec = len(name)
    name = [name[k].strip() for k in range(nspec)]
    iSpecies = name.index(whichSpecies)
    
    #2nd line is total gas pressure label and value
    inLine1 = inputHandle.readline()
    fields = inLine1.split()
    pt = float(fields[1].strip())
    print("pt ", pt)
    
    #3rd line is labels
    inLine1 = inputHandle.readline()
        
    #Loop through temperature blocks:
    while (inLine1 != ""):
        
        inLine1 = inputHandle.readline()
        #print(inLine)
        if not inLine1:
            break
        
        numTemp+=1
        
        #1st repeating line is t   rholog   gmu   fd   fe values
        fields = inLine1.split()
        t.append(float(fields[0].strip()))
        rholog.append(float(fields[1].strip()))
        gmu.append(float(fields[2].strip()))
        fd.append(float(fields[3].strip()))
        fe.append(float(fields[4].strip()))
        
        #Next (looooong) repeating is the nspece log10(pp/pt) values
        inLine2 = inputHandle.readline()
        thisFp = inLine2.split()
        thisFp = [float(thisFp[k].strip()) for k in range(nspec)]
        thisPp = [pt*(10.0**thisFp[j]) for j in range(len(thisFp))]
        fp.append(thisFp)
        pp.append(thisPp)
        #print("numTemp ", numTemp, " thisFp ", thisFp)

print("Species: ", iSpecies, name[iSpecies])       
print("t ", t)
#print("fp[which] ", [fp[k][iSpecies] for k in range(numTemp+1)])
#print("pp[which] ", [pp[k][iSpecies] for k in range(numTemp+1)])  

#Plot some partial pressures:
# Issue 'matplotlib qt5' in console before running code
        
titleString = "$\log P=$" + str(int(math.log10(pt)))
plt.title(titleString)
plt.ylabel('$\log P_*/P$')
plt.xlabel('$T$ (K)')
xMin = min(t)
xMax = max(t)
#pylab.xlim(xMin, xMax)
#pylab.ylim(-9.0, 0.5)        
#pylab.plot(t, [fp[k][iSpecies] for k in range(numTemp+1)], color="black")
plt.xlim(xMin, xMax)
plt.ylim(-9.0, 0.5)        
plt.plot(t, [fp[k][iSpecies] for k in range(numTemp+1)], color=colorCode)

#annotation:
thisT = t[numTemp-5]
thisFp = fp[numTemp-5][iSpecies] + 0.75
#pylab.text(thisT, thisFp, name[iSpecies])
plt.text(thisT, thisFp, name[iSpecies])

"""
#add the line IDs
for i in range(numLineIds):
    if "Ca II" in lblIds[i]:
        thisLam = waveIds[i]
        thisLbl = lblIds[i]
        xPoint = [thisLam, thisLam]
        yPoint = [1.05, 1.1]
        pylab.plot(xPoint, yPoint, color='black')
        pylab.text(thisLam, 1.5, thisLbl, rotation=270)

#Save as encapsulated postscript (eps) for LaTex
epsName = fileStem + '.eps'
plt.savefig(epsName, format='eps', dpi=1000)        
"""        
#End
        

        

        
        
         

        
    

    

  