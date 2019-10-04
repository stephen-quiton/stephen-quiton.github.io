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
cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
execute_next = 'python ../../next_job.py ../../' + input1[0:4] + '.out'
copy_to_subdir = 'cp ' + input2 + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'python ../../custodian.py ' + input2 + ' "$TMPDIR" && '
copy_output_maindir = 'cp ' + input2[0:-4] + '.out ../../'
full_script = cd_subdir + execute_next + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir
firetask = ScriptTask.from_str(full_script)
FreqJobFW = Firework(firetask, name = 'QChem Freq',fw_id=2)

#Add workflow to launchpad
workflow = Workflow([OptJobFW, FreqJobFW],{1:[2]}, name = 'QChem-Opt2Freq')
launchpad.add_wf(workflow)
