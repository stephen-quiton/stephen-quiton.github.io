---
layout: default
---

## Running your First Workflow

[Previous](./FW2-Required-Files.html)| [Home](../) | [Next](./FW4-Advanced-Setups.html)

Now that we have all of the files required for launch, we're almost ready to launch. First thing is to actually add information about our workflow to the MongoDB launchpad. There's many ways to do so, but I think it would be good if we use *python* because it can allow us to easily make complex workflow patterns; more on that later. For this tutorial, we're just going to make a workflow that executes a single firework.

### Python Script to add Workflow

Create a python script file, name it whatever (add_wf.py), and place the following in it. Some of the syntax will be confusing at first because I didn't give you certain information beforehand, but for now, just trust me: 


```python
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
```


### Launch!

### Dealing with FireWorks in Offline Mode

The FireWorks tutorial has several ways of adding a workflow to the database and also several ways to run it (for instance: `rlaunch singleshot`, `qlaunch singleshot`, etc.). Since we want to eventually run a lot of jobs at once, let's stick to `qlaunch rapidfire`


[Previous](./FW1-PythonInst.html) | [Home](../) | [Next](./FW4-Advanced-Setups.html)

