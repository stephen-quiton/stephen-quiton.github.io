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

input = 'methane.inp' #replace with your qchem input file name

#These lines are shell commands that need to be executed sequentially 
cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
copy_to_subdir = 'cp ' +  input + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'qchem -nt 20 ' + input + ' && '
copy_output_maindir = 'cp ' + input[0:-4] + '.out ../../'
  
#Each line combined into one huge script. '&&' serves to separate commands
full_script = cd_subdir + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir

#Create a ScriptTask that takes a shell command string as its argument
firetask = ScriptTask.from_str(full_script)   
#use the ScriptTask object as an argument to create a Firework object
firework= Firework(firetask, name = 'Methane SPE',fw_id=1)
#Use the Firework object as an argument to create a Workflow object
workflow = Workflow([firework], name = 'Methane')
#Add Workflow object to launchpad 
launchpad.add_wf(workflow) 