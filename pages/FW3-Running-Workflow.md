---
layout: default
---

# Running your First Workflow

[Previous](./FW2-Required-Files.html)| [Home](../) | [Next](./FW4-Advanced-Setups.html)

Now that we have all of the files required for launch, we're almost ready to launch. First thing is to actually add information about our workflow to the MongoDB launchpad. There's many ways to do so, but I think it would be good if we use *python* because it can allow us to easily make complex workflow patterns; more on that later. For this tutorial, we're just going to make a workflow that executes a single firework.

### Python Script to add Workflow

Create a python script file, name it whatever (add_wf.py), and place the following in it. Some of the syntax will be confusing at first because I didn't give you certain information beforehand, but hopefully the comments will make things clearer:

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

input = 'methane.inp' #replace with your qchem input file name

#These lines are shell commands that need to be executed sequentially
cd_subdir = 'cd $SLURM_SUBMIT_DIR && '
copy_to_subdir = 'cp ' +  input + ' $SLURM_SUBMIT_DIR && '
source_qchem = 'source /usr/usc/qchem/default/qcenv.sh && '
exec_qchem = 'qchem -nt 20 ' + input + ' && '
copy_output_maindir = 'cp ' + input[0:-4] + '.out ../../'

#Each line is combined into one long command. '&&' serves to separate individual commands
full_script = cd_subdir + copy_to_subdir + source_qchem + exec_qchem + copy_output_maindir

#Create a ScriptTask that takes a shell command string as its argument
firetask = ScriptTask.from_str(full_script)   
#use the ScriptTask object as an argument to create a Firework object
firework= Firework(firetask, name = 'Methane SPE',fw_id=1)
#Use the Firework object as an argument to create a Workflow object
workflow = Workflow([firework], name = 'Methane')
#Add Workflow object to launchpad
launchpad.add_wf(workflow)
```
Once you have `add_wf.py`, execute it. But before that, reset the launchpad:

```
lpad reset
python add_wf.py
```

To check if the workflow was correctly added to the MongoDB launchpad, it should have returned a short message entailing that a Firework had been added. You can also use the following command below

```shell
lpad -l my_launchpad.yaml get_wflows
```
As you may have noticed, the `-l` option specifies the launchpad YAML file to use to connect to the database, and you need it everytime you execute `lpad`. Technically, you don't actually have to specify `-l` if you named your launchpad file `my_launchpad.yaml` and did `lpad` in the same directory (see [this](https://materialsproject.github.io/fireworks/queue_tutorial.html#submit-a-job) for more info). But, if you wanted to run lpad outside of this particular directory you can save yourself some typing by adding the following to your .bashrc:

```shell
alias lpad='lpad -l /path/to/my_launchpad.yaml'
```

### Launch!

Now that you've added your workflow, you can now launch. Run the following
```
qlaunch -r rapidfire -m 1
```
To check if it's running, use `squeue` or `sacct`.

The main FireWorks tutorial has several ways of launching a workflow (for instance: `rlaunch singleshot`, `qlaunch singleshot`, etc.). Since we want to eventually run a lot of jobs at once and because it has a specific behavior in terms of organizing job files, let’s stick to `qlaunch rapidfire`.

### Dealing with FireWorks in Offline Mode



[Previous](./FW1-PythonInst.html) | [Home](../) | [Next](./FW4-Advanced-Setups.html)
