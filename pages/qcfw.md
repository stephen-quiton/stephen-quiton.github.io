---
layout: default
---

# Explanation of QCFW functions

[Home](../)

These are functions that allow me to run QChem while taking advantage of the full capabilities of FireWorks, namely, uploading and passing important information to the database. Here I go through a function-by-function walkthrough of functions.py.

```python
import json,multiprocessing

from pymatgen.io.qchem.inputs import QCInput
from pymatgen.io.qchem.outputs import QCOutput
from pymatgen.core import Molecule

from custodian.custodian import Custodian
from custodian.qchem.handlers import QChemErrorHandler
from custodian.qchem.jobs import QCJob

def QCOutput_to_encode(qcoutput,more_info=None):
    """ Converts a qcoutput object to an encoding
    from a .out file.
    """
    #Default recorded info
    requested_info = ['final_energy','errors','initial_geometry','last_geometry', 'species','charge','multiplicity']
    requested_info.append(more_info)

    data = {}
    # Assemble the compressed dictionary of results
    for info in qcoutput.as_dict()['data'].keys():
        if info in requested_info:
            data[info] = qcoutput.as_dict()['data'][info]
    # Return the reduced results in JSON compression
    return json.dumps(data)
```    
This first function takes a pymatgen QCOutput object as an input and converts the requested information in `requested_info` (which you can add to via the list argument `more_info`) into a json-format encoding string, which is database-friendly. This is needed not only so that we can later upload this string to the database and see the info on the webgui, but also so that other fireworks can use this information to construct new input files. The leads to the next function:

```python    
def encode_to_QCInput(encode,rem,pcm=None,solvent=None):
    """Takes final geometry from encode, creates QCInput object
    """
    data = json.loads(encode, encoding='utf-8')
    
    try:
        opt_geom = Molecule(
            species=data.get('species'),
            coords=data.get('last_geometry'),
            charge=data.get('charge'),
            spin_multiplicity=data.get('multiplicity'))
    except KeyError:
         opt_geom = Molecule(
            species=data.get('species'),
            coords=data.get('initial_geometry'),
            charge=data.get('charge'),
            spin_multiplicity=data.get('multiplicity'))       
       
    NewInput = QCInput(molecule = opt_geom,rem=rem,pcm=pcm,solvent=solvent)
    return NewInput
 
```
This function is like the inverse of the previous one. It takes the optimized geometry (or initial geometry if not an optimization) from the encoding string and a user-provided rem dict (containing the necessary qchem keys for your next job) to construct a QCInput object. Later we will call this QCInput's write_file method to obtain our input file.

```python
def run_QChem(label,encode=None,rem=None,pcm=None,solvent=None,more_info=None):
    inname = label + '.inp'
    outname = label + '.out'
    logname = label + '.log'
    handlers = [QChemErrorHandler(input_file=inname,output_file=outname)]
    """if no encoding provided, assume first Firework in workflow and that input file is already written
    'label' is the name of the file without the extension (e.g. .inp, .out). otherwise, take encoding, 
    form new QCInput and write input file, then run.
    """   
    if encode!= None:
        qcin = encode_to_QCInput(encode=encode,rem=rem,pcm=pcm,solvent=solvent)
        qcin.write_file(inname)
    
    command='qchem'
    jobs = [
        QCJob(
            input_file=inname,
            output_file=outname,
            qchem_command = command,
            max_cores = multiprocessing.cpu_count(),
            qclog_file=logname
        )
    ]
    c = Custodian(handlers, jobs, max_errors=10)
    c.run()

    output = QCOutput(filename=outname)
    return QCOutput_to_encode(output,more_info=more_info)
```
This is the primary function that is to be run as its own pytask; it takes a label (which is the name of your input file without .inp), performs a Custodian-corrected qchem job, and returns the results in a json encoding. 

An important note is if the user provides the encoding string, that implies that the input file for that firework has not been generated; Conversely, if you already have your input file ready (which is usually the first firework in the workflow), then there is no need to provide an encoding from which to obtain an optimized geometry. Let's take the example from the main tutorial:


```python
freqRem ={
    'basis':'6-31G',
    'job_type':'freq',
    'exchange':'b3lyp',
    'scf_convergence':'8',
    'sym_ignore':'true',
}
opt_label = 'qchem_opt' 
freq_label = 'qchem_freq'
label = 'qchem'
#Construct Firework 1: Optimization
t0 = PyTask(
    func='qcfw.functions.run_QChem',
    kwargs={'label':opt_label},
    outputs = ['output_encoding'],
    )
optFW = Firework([t0], spec={'_priority': 1}, name=opt_label,fw_id=1)
#Construct Firework 2: Frequency
t1 = PyTask(
    func='qcfw.functions.run_QChem',
    args=[freq_label],
    kwargs={'rem':freqRem},
    stored_data_varname='parsed_data',
    inputs = ['output_encoding'],
    )        
freqFW = Firework([t1], spec={'_priority': 1}, name=freq_label,fw_id=2)
```
In 
[Home](../)
