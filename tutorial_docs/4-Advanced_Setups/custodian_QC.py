#A Custodian wrapper for QChem jobs. Intended to be run from SLURM. Effectively replaces 'qchem mol.inp'
import sys
sys.path.append('/path/to/your/python3.6/site-packages') #Replace
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