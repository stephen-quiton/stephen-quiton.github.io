from fireworks.core.firework import Firework, Workflow
from fireworks.core.fworker import FWorker
from fireworks.core.launchpad import LaunchPad
from fireworks.user_objects.firetasks.script_task import ScriptTask

launchpad = LaunchPad(
    host = 'cluster0-shard-00-0x-abcde.azure.mongodb.net', #replace
    authsource = 'admin',
    name = 'put-any-name', #replace
    password = 'mongo-password', #replace
    ssl = True,
    username = 'mongo-username' #replace
) 

input = 'Methane.inp' #replace

cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
copy_to_subdir = 'cp ' +  input + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'qchem -nt 20 ' + input + ' && '
copy_output_maindir = 'cp ' + input[0:-4] + '.out'
  
full_script = cd_subdir + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir
 
firetask = ScriptTask.from_str(full_script)   
firework= Firework(firetask, name = 'Methane SPE',fw_id=1)
workflow = Workflow([firework], name = 'Methane')
launchpad.add_wf(workflow)
    