---
layout: default
---

# Advanced Setups
[Previous](./FW3-Running-Workflows.html) | [Home](../) | [Next](./FW5-WebGUI.html)

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
[Custodian](https://materialsproject.github.io/custodian/) is another useful python packages that can be used to create wrappers for various quantum chemistry codes and enabling them to automatically correct commonly encountered errors. You can view the full list of errors it corrects for QChem [here](https://github.com/materialsproject/custodian/blob/master/custodian/qchem/handlers.py)

Installing it is just like our previous packages. I recommend you do this in a separate directory:

```
pip install custodian --user
```

As for wrapping our QChem job, it's a relatively short script. But before that, transfer over your own qchem input qchem.inp (preferably a short geometry optimization) and put the following error-inducing parameter in the $rem section:

```
max_scf_cycles = 2
```
Then, create the following python script (custodian.py)

```python
#A Custodian wrapper for QChem jobs. Intended to be run from SLURM. Effectively replaces 'qchem mol.inp'
import sys
sys.path.append('/path/to/your/python3.6/site-packages')
from custodian.custodian import Custodian
from custodian.qchem.handlers import QChemErrorHandler
from custodian.qchem.jobs import QCJob

inname = sys.argv[1] #name of the input file
outname = inname[0:-4] + '.out'
logname = inname[0:-4] + '.log'
handlers = [QChemErrorHandler(input_file=inname,output_file=outname)]

#Setup variables for the QCJob
scratch_dir = sys.argv[2] #Need to transfer the scratch directory
command = "qchem"
max_cores = 20

jobs = [
        QCJob(
            input_file=inname,
            output_file=outname,
            qchem_command = command,
            max_cores = max_cores,
            scratch_dir = scratch_dir,
            qclog_file=logname
        )
    ]
c = Custodian(handlers, jobs, max_errors=10)
c.run()
```

For this, we're not going to execute this python script from the command line. We are actually going to use a SLURM run script to execute it, so we can demonstrate how we can incorporate this into the main FireWorks framework. Copy the following from below and place it into a shell script (custodian.run).

```shell
#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --time=12:00:00
#SBATCH --partition=sharada
#SBATCH --job-name=qchem.inp
#SBATCH --output=qchem.out
#SBATCH --mem-per-cpu=2GB

export QC=/usr/usc/qchem/default
export QCAUX=$QC/qcaux
export QCPLATFORM=LINUX_Ix86_64
export QCRSH=ssh
export PATH=$QC/bin:$PATH
export QCSCRATCH=$TMPDIR

cd ${SLURM_SUBMIT_DIR}
source /usr/usc/qchem/default/qcenv.sh
python custodian.py qchem.inp "$TMPDIR"
cp -R "$TMPDIR" "$SLURM_SUBMIT_DIR"
```
Then submit it using `sbatch`. Check back a couple of minutes later, and you should have a couple of new files aside from `qchem.out`, including `custodian.json`. This contains all of the errors Custodian picked up and the measures it took to correct it. For our case, the job should have ran into an error due to too few SCF cycles, to which Custodian should have responded by simply increasing it.


### Running Multi-firework Workflows

[Previous](./FW3-Running-Workflows.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW5-WebGUI.html)
