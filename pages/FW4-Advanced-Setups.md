---
layout: default
---

# Advanced Setups
[Previous](./FW3-Running-Workflow.html) | [Home](../) | [Next](./FW5-WebGUI.html)

Chances are that you're not using FireWorks just to run one workflow containing a single job. At the very least, you're looking forward to running many of these calculations at once and/or create more intricate workflows where each firework depends on information contained in the previous job. Perhaps you'd also be interested in giving your QChem jobs some ability to self correct in errors.

All of these aspects will be addressed in this section, with the introduction of two python packages (also made by the Materials Project) and utilizing them to create more complex workflows. 

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
python custodian.py qchem_custodian.inp "$TMPDIR"
cp -R "$TMPDIR" "$SLURM_SUBMIT_DIR"
```
Then submit it using `sbatch`. Notice how this is the exact same run script as a normal QChem SLURM submission, except the `qchem` execution line is replaced with an execution of our Custodian script. For the `python` line, you may see that we have some additional input arguments; these exist so that we are able to pass the name of the input file as well as the scratch directory (``"$TMPDIR"``) to Custodian via `sys.argv`.

Check back a couple of minutes later, and you should have a couple of new files aside from `qchem.out`, including `custodian.json`. This contains all of the errors Custodian picked up and the measures it took to correct it. For our case, the job should have ran into an error due to too few SCF cycles, to which Custodian should have responded by simply increasing it.

## Running Multi-firework Workflows

Now let's see how we can incorporate both of these features into implementing more workflows. Open up to another empty directory and place your .yaml files (`my_launchpad`, `my_qadapter`, `my_fworker`, `my_qadapter`) and a copy of the `custodian.py` we wrote. Also place a qchem input that's a geometry optimization (like `methane.inp`). What we are going to do is utilize both Custodian and Pymatgen to create a workflow that proceeds from an initial geometry optimization to a frequency job. In order to do so, not only do we need the previous files I mentioned, but also 2 more: one to handle passing information from an output to an input, and another to add the workflow to the database (which we have written before in `add_wf.py` but this time it's different).

#### next_job.py
This script is not to be executed manually by the user from the command line, but from the SLURM run script of the second job. You'll see what I mean once we take a look at its contents:
```python
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
       "BASIS":"def2-svpd"
       "GUI": "2"
       "JOB_TYPE": "freq"
       "METHOD":"B3LYP"
    }
    NewPCM = None #can contain a PCM dict
    NewSolv = None #can contain a SOLV dict 
    NewInput = QCInput(molecule = opt_geom, rem = NewRem, pcm = NewPCM, solvent = NewSolv)
    NewInput.write_file("qchem_freq.inp") #put whatever name here

NextJob(fname = input1)
```

So essentially, when this script is called by `python next_job.py "qchem_opt.out"`, it takes the optimized geometry of `qchem_opt.out` and uses that to create a new frequency input file. You'll see how this comes into play in our next required script.

#### add_multi_wf.py

```python
from fireworks.core.firework import Firework, Workflow
from fireworks.core.fworker import FWorker
from fireworks.core.launchpad import LaunchPad
from fireworks.user_objects.firetasks.script_task import ScriptTask

#create LaunchPad object using your own info
launchpad = LaunchPad(
    host = 'cluster0-shard-00-0x-abcde.azure.mongodb.net', #replace
    authsource = 'admin',
    name = 'put-any-name', #replace
    password = 'mongo-password', #replace
    ssl = True,
    username = 'mongo-username' #replace
)

input1 = 'qchem_opt.inp' #replace with your qchem input file name
input2 = 'qchem_freq.inp' #replace with your qchem input file name

#Construct Firework 1: Optimization
cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
copy_to_subdir = 'cp ' + input1 + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'python ../../custodian.py ' + input1 + ' "$TMPDIR" && '
copy_output_maindir = 'cp ' + input1[0:-4] + '.out ../../'
full_script = cd_subdir + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir
firetask = ScriptTask.from_str(full_script)
OptJobFW = Firework(firetask, name = 'QChem Opt',fw_id=1)

#Construct Firework 2: Frequency
execute_next = 'python next_job.py ' + input1[0:4] + '.out'
cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
copy_to_subdir = 'cp ' + input2 + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'python ../../custodian.py ' + input2 + ' "$TMPDIR" && '
copy_output_maindir = 'cp ' + input2[0:-4] + '.out ../../'
full_script = cd_subdir + execute_next + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir
firetask = ScriptTask.from_str(full_script)
FreqJobFW = Firework(firetask, name = 'QChem Freq',fw_id=2)

#Add workflow to launchpad
workflow = Workflow([Freq2FW,Opt2FW,Freq1FW,Opt1FW],{1:[2]}, name = 'QChem-Opt2Freq')
launchpad.add_wf(workflow)
```

In this script, I would like to highlight three main differences from the previous,  similar `add_wf.py` that we wrote last time.

1. We construct two separate fireworks, one containing a firetask that executes the first optimization job, and the other containing the same firetask that executes the second frequency job. These two fireworks are then wrapped into the same workflow in the last lines.
2. In the second firework, we add a command stored in `execute_next` that executes `next_job.py`, which should automatically generate the frequency job input.
3. Instead of the usual QChem execution line `qchem -nt 20 file.inp`, we replace it with an execution of `custodian.py`. Doing this gives the job some self- correcting ability. 

#### Execution

Like last time, run 

```shell
python add_multi_wf.py
```

which should result in a single workflow containing two fireworks being added to the launchpad.   With that, all files and workflows should be in place; all that's left is to execute

```shell
qlaunch -r rapidfire -m 24
```

The rocket should have been launched. Keep this terminal on (if you shut it off, the  ) and open another one. If you run `lpad get_fws`, you should see a firework somewhere called 'QChem Opt' that has been set to the 'RESERVED' state. This is true if your job is in the pending state (which you can see via `squeue` or `sacct`) and the partition you submitted to is backlogged. But if you find that it's actually running, then the 'RESERVED' state is incorrect. This is due to the fact that we have to run Fireworks offline, which I talked about in the previous section. 

To refresh and update the state, run

```shell
lpad recover_offline
```

After a few seconds, check `lpad get_fws` and it should read either 'RUNNING' or 'COMPLETED' depending on if your job actually finished. If it is completed, that means the next frequency job is ready to run and as long as you kept that other terminal running `qlaunch` open, you do not have to do anything; it will be launched automatically. If you accidentally closed it, you can just run the `qlaunch` command again. 

As with the previous firework, you can run `lpad recover_offline` to refresh the state until it completes. When it does, you should have a QChem frequency output `qchem_freq.out`, thereby completing the entire workflow.

### The End (Or is it?)

Congratulations again! You've just made a workflow that not only passes information from one job to the next, but also gave them some self-correcting ability. As you can imagine, you can extend these examples to your case and you can also utilize more features of FireWorks to your advantage, some of which include:

1. [Writing custom firetasks](https://materialsproject.github.io/fireworks/guide_to_writing_firetasks.html#)
2. Using pymatgen to perform [ligand/molecule substitutions](http://pymatgen.org/pymatgen.core.structure.html?highlight=substitute#pymatgen.core.structure.Molecule.substitute)
3. Creating your own WebGUI to track your jobs, which I will explain in the next tutorial 

And there's certainly more ways to accomplish the same objectives as the workflow we made above. For instance, instead of wrapping one giant command into each firework, you could have made tiny ScriptTasks and wrapped all of those into one firework. Or (I have not done this myself but I believe it's possible) you can pass information via [updating the spec](https://materialsproject.github.io/fireworks/guide_to_writing_firetasks.html#the-fwaction-object). 

In essence, my tutorials are hopefully good suggestions on how to setup your jobs; but as far as adapting them to your case, that is left to your discretion









[Previous](./FW3-Running-Workflow.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW5-WebGUI.html)

