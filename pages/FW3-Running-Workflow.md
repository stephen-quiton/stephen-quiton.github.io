---
layout: default
---

## Running your First Workflow

[Previous](./FW1-PythonInst.html)| [Home](../) | [Next](./FW4-Advanced-Setups.html)

Now that we have set-up FireWorks on HPC and have a working connection to our 'launchpad' hosted on MongoDB, we can now prepare to launch our first workflow. In order to do so, however, we need to create some files. 

### Required YAML files
Open up to an empty directory (or the same one your `my_launchpad.yaml` is located). Create the following .yaml files:

#### my_launchpad.yaml
This file contains all the necessary information for your FireWorks installation to connect to your launchpad via `lpad` (used to query your database for existing workflows and other tasks) , `qlaunch` (launch fireworks in queue in succession), etc. We'll get to use these commands later on. 

If you have already created this file from the [previous page](./FW1-PythonInst.html) and have it in the directory already, then you're good to go. In case you haven't, you can copy paste from below and replace the information with your own:

```
authsource: admin
host: cluster0-shard-00-0x-abcdef.azure.mongodb.net
logdir: null
name: put-any-name
password: mongo-password
port: 27017
ssl: true
ssl_ca_certs: null
ssl_certfile: null
ssl_keyfile: null
ssl_pem_passphrase: null
strm_lvl: INFO
user_indices: []
username: mongo-username
wf_user_indices: []
```

#### my_fworker.yaml

This file is used so that FireWorks can write to the launchpad the user that launched the particular firework. Its contents are very short:

```
name: Put-any-name
category: ''
query: '{}'
```

#### my_qadapter.yaml

This is used to 

```

```
###

### Python Script to add Workflow

### Launch!

### Dealing with FireWorks in Offline Mode

The FireWorks tutorial has several ways of adding a workflow to the database and also several ways to run it (for instance: `rlaunch singleshot`, `qlaunch singleshot`, etc.). Since we want to eventually run a lot of jobs at once, let's stick to `qlaunch rapidfire`


[Previous](./FW1-PythonInst.html) | [Home](../) | [Next](./FW4-Advanced-Setups.html)

