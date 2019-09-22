---
layout: default
---
[Previous](./FW3-Running-Workflowss.html) | [Home](../) | [Next](./FW5-WebGUI.html)
# Advanced Setups

Chances are that you're not using FireWorks just to run one workflow containing a single job. At the very least, you're looking forward to running many of these calculations at once and/or create more intricate workflows where each firework depends on information contained in the previous job. Perhaps you'd also be interested in giving your QChem jobs some ability to self correct in errors.

All of these aspects will be addressed in this section, with the introduction of two python packages (also made by the Materials Project) and utilizing them to create more complex workflows

### Pymatgen
[Pymatgen](http://pymatgen.org/) is another python package that can perform input/output parsing for various quantum chemistry codes, including QChem. You can either install it via
```shell
conda install --channel matsci pymatgen
```
or:
```shell
pip install pymatgen --user
```

Once you've done it, open up to an empty directory and place the following python script (transfer_geom.py) along with a sample qchem output file qchem.out (preferably a successful geometry optimization) for a demonstration of parsing outputs and generating inputs:

```python
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
```

Execute the above python script. By the end, you should be able to see a new input "NewInp.inp" with the last optimized geometry of your given output and some new $rem parameters. Using pymatgen's QCInput and QCOutput objects, we can easily transfer key information like geometries between fireworks and also extract data en masse from outputs.

### Custodian


### Running Multi-firework Workflows

[Previous](./FW3-Running-Workflowss.html) | [Home](../) | [Next](./FW5-WebGUI.html)
