#!/usr/bin/env python
import sys
sys.path.append('/path/to/your/python3.6/site-packages')
sys.path.append('/path/to/your/python2.7/site-packages')

from fireworks.core.firework import FWAction, Firework, FiretaskBase
import pymatgen
from pymatgen.io.qchem.inputs import QCInput
from pymatgen.io.qchem.outputs import QCOutput
from fireworks.core.launchpad import LaunchPad

input1 = sys.argv[1] #previous output file name with quotes

def NextJob(fname):
    output = QCOutput(filename = fname)
    opt_geom = output.data['molecule_from_last_geometry']
    NewRem = {
       "BASIS":"def2-svpd",
       "GUI": "2",
       "JOB_TYPE": "freq",
       "METHOD":"B3LYP"
    }
    NewPCM = None #can contain a PCM dict
    NewSolv = None #can contain a SOLV dict
    NewInput = QCInput(molecule = opt_geom, rem = NewRem, pcm = NewPCM, solvent = NewSolv)
    NewInput.write_file("qchem_freq.inp") #put whatever name here

NextJob(fname = input1)
