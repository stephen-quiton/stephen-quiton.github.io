---
layout: default
---

# Required files

[Previous](./FW1-PythonInst.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW3-Running-Workflow.html)

Now that we have set-up FireWorks on HPC and have a working connection to our 'launchpad' hosted on MongoDB, we can now prepare to launch our first workflow. In order to do so, however, we need to create some files. These can all be found on the main FireWorks tutorial, but I've adjusted them for our case.


Open up to an empty directory (or the same one your `my_launchpad.yaml` is located). By the end of this, we should have the following.

1. my_launchpad.yaml
2. my_fworker.yaml
3. my_qadapter.yaml
4. SLURM_Template.txt
5. methane.inp


#### my_launchpad.yaml
This file contains all the necessary information for your FireWorks installation to connect to your launchpad via `lpad` (used to query your database for existing workflows and other tasks) , `qlaunch` (launch fireworks to a queueing system, like SLURM, in succession), etc. We'll get to use these commands later on.

If you have already created this file from the [previous page](./FW1-PythonInst.html) and have it in the directory already, then you're good to go. In case you haven't, you can copy paste from below and replace the information with your own:

```yaml
authsource: admin
host: cluster0-shard-00-0x-abcde.azure.mongodb.net #replace
logdir: null
name: put-any-name #replace
password: mongo-password #replace
port: 27017 #default, but replace if different
ssl: true
ssl_ca_certs: null
ssl_certfile: null
ssl_keyfile: null
ssl_pem_passphrase: null
strm_lvl: INFO
user_indices: []
username: mongo-username #replace
wf_user_indices: []
```

#### my_fworker.yaml

This file is used so that FireWorks can write to the launchpad the user that launched the particular firework. Its contents are very short:

```yaml
name: Put-any-name
category: ''
query: '{}'
```



#### SLURM_Template.txt and my_qadapter.yaml
For this step, we'll create two separate files, both of which will enable us to make our jobs work with SLURM's queuing system. It's necessary if we want to launch jobs via `qlaunch`, not just `rlaunch` (the normal way to launch FireWorks). First, we create `SLURM_template.txt` which looks like this:

```shell
#!/bin/bash -l

#SBATCH --nodes=$${nodes}
#SBATCH --ntasks=$${ntasks}
#SBATCH --ntasks-per-node=$${ntasks_per_node}
#SBATCH --ntasks-per-core=$${ntasks_per_core}
#SBATCH --exclude=$${exclude_nodes}
#SBATCH --cpus-per-task=$${cpus_per_task}
#SBATCH --gres=$${gres}
#SBATCH --qos=$${qos}
#SBATCH --time=$${walltime}
#SBATCH --partition=$${queue}
#SBATCH --account=$${account}
#SBATCH --job-name=$${job_name}
#SBATCH --license=$${license}
#SBATCH --output=$${job_name}.out
#SBATCH --constraint=$${constraint}
#SBATCH --signal=$${signal}
#SBATCH --mem=$${mem}
#SBATCH --mem-per-cpu=$${mem_per_cpu}


export QC=/usr/usc/qchem/default
export QCAUX=$QC/qcaux
export QCPLATFORM=LINUX_Ix86_64
export QCRSH=ssh
export PATH=$QC/bin:$PATH
export QCSCRATCH=$TMPDIR

$${pre_rocket}
$${rocket_launch}
$${post_rocket}
cp -R "$TMPDIR" "$SLURM_SUBMIT_DIR"

# CommonAdapter (SLURM) completed writing Template

```

As the title suggests, this file is the .run file template that will be used everytime you launch a firework. The export lines are specifically for QChem, and may be different depending on what code you're using. Take notice of all the `$${job}` parameters we can modify. This is what our next file `my_qadapter.yaml` is for:

```yaml
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -w /path/to/my_fworker.yaml -l /path/to/my_launchpad.yaml singleshot --offline
ntasks: null
cpus_per_task: 1
nodes: 1
mem_per_cpu: 2GB
ntasks_per_node: 20
walltime: '12:00:00'
queue: null #change to your partition
account: null
job_name: null
logdir: /auto/rcf-40/quiton/fw_logs/
pre_rocket: null
post_rocket: null

# You can override commands by uncommenting and changing the following lines:
# _q_commands_override:
#    submit_cmd: my_qsubmit
#    status_cmd: my_qstatus

#You can also supply your own template by uncommenting and changing the following line:
_fw_template_file: /path/to/SLURM_template.txt
```
Take notice of the `rocket_launch` line where you'll have to specify the _absolute_ paths to your fworker and launchpad yaml files. Same goes for `_fw_template_file`, with the path pointing to the SLURM_template we just made. The --offline option I will explain later, but keep that. Also, you can change `queue` to match your particular partition.

#### QChem Input (methane.inp)
Finally, you'll need your actual QChem input file. For the sake of speed, let's do a single point of methane:

```
$molecule
0 1
C    0.00000    0.00000   -0.00000
H    0.61776   -0.61776    0.61776
H    0.61776    0.61776   -0.61776
H   -0.61776    0.61776    0.61776
H   -0.61776   -0.61776   -0.61776
$end

$rem
JOBTYPE spe
METHOD b3lyp
BASIS 6-31G
$end
```
Since we're using FireWorks to launch via SLURM, we do not need a `.run` file.

[Previous](./FW1-PythonInst.html) <code>&#124;</code> [Home](../) <code>&#124;</code> [Next](./FW3-Running-Workflow.html)
