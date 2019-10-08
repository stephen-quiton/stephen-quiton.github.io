from pymatgen.io.qchem.inputs import QCInput
from pymatgen.io.qchem.outputs import QCOutput

#convert output into QCOutput object
output = QCOutput(filename = "qchem.out")

#extract optimized geometry
opt_geom = output.data['molecule_from_last_geometry']

#manually create job parameters for $rem
NewRem = {
   "BASIS":"def2-svpd"
   "GUI": "2"
   "JOB_TYPE": "opt"
   "METHOD":"B3LYP"
}

#Use these to construct QCInput object
NewInput = QCInput(molecule = OptBenz, rem = NewRem)

#Write new input file
NewInput.write_file("NewInp.inp")