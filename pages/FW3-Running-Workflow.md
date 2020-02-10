---
layout: default
---

# Running your First Workflow

[Previous](./FW2-Required-Files.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW4-Advanced-Setups.html)

Now that we have all of the files required for launch, we're almost ready to launch. First thing is to actually add information about our workflow to the MongoDB launchpad. There's many ways to do so, but I think it would be good if we use *python* because it can allow us to easily make complex workflow patterns; more on that later. For this tutorial, we're just going to make a workflow that executes a single firework.

### Python Script to add Workflow

Create a python script file, name it whatever (add_wf.py), and place the following in it. Some of the syntax will be confusing at first because I didn't give you certain information beforehand, but hopefully the comments will make things clearer:

```python
from fireworks import LaunchPad, Firework, Workflow, PyTask
#create LaunchPad object using your own info
launchpad = LaunchPad(
    host = 'localhost',
    port = 27017,#default, replace with yours
    authsource = 'admin',
    name = 'fireworks',
    password = None,
    ssl = False,
    username = None
)
input = 'methane.inp' #replace with your qchem input file name

label = inp[0:-4]
t0 = PyTask(
    func='qcfw.functions.run_QChem',
    kwargs={'label':label},
    outputs = ['output_encoding']
    )
fw0 = Firework([t0], spec={'_priority': 1}, name=label,fw_id=1)    
wf = Workflow ([fw0],name=label)
launchpad.add_wf(wf)
```

So in essence, this workflow will replace the $${rocket_launch} value in the SLURM template with the execution of the run_QChem function with the input being the name of the input file without the extension

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
Something you might have also noticed was the `-r` option in the `qlaunch` command. This means launch in reserve mode, which is required for our setup because we must run FireWorks in [offline mode](https://materialsproject.github.io/fireworks/offline_tutorial.html). This is because HPC's compute nodes are not able to connect to the internet directly.

This will not affect the normal operation of FireWorks apart from one aspect: that you'll have to run a command to update whether a given firework is in the "RUNNING", "COMPLETED", or "FIZZLED" states.  

Once your job is complete via `sacct`/`squeue`, run `lpad get_wflows`. It should read that the state of your firework had been automatically set to "RESERVED" (meaning that the job was pending, but is not running), but not "COMPLETED". Then run the following

```
lpad recover_offline
```

Now check your job status again, and it should be correctly marked "COMPLETED". This affects our jobs in that if Firework A leads to Firework B, Firework B will not begin until Firework A has been marked "COMPLETED".

**Congratulations!** You've just run your first workflow! Now we can get on to a slightly more advanced setup, which takes advantage of even more of FireWorks capabilities.


[Previous](./FW2-Required-Files.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW4-Advanced-Setups.html)
