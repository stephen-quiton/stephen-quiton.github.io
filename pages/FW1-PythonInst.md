---
layout: default
---

# Installing FireWorks and Setting up MongoDB

[Home](../) <code>&#124;</code> [Next](./FW2-Required-Files.html)

### FireWorks

Installing python packages on HPC is [not necessarily the same](https://hpcc.usc.edu/support/documentation/python/) as if you were to do the same with your own machine. This is because the command `pip` usually goes to a directory guarded by sudo permissions, which we don't have. Thus, the commands we need to use are:

```shell
source /usr/usc/python/3.6.0/setup.sh
pip install FireWorks --user
```

I highly recommend you place the first line in your `~/.bashrc` so python is setup when you enter the shell. With the `--user` option, the FireWorks python package should be installed to `~/.local`. You can keep .local where it is if you'd like, but I've decided to make `~/.local` a soft-link to a directory with more quota space so I don't have to be concerned with storage.

To test if FireWorks is installed correctly, restart your terminal and run the command `lpad`. If it returns with a list of options to use with `lpad`, you're ready to go

### MongoDB

Although we could use a third party server to host our MongoDB (which is what I did formerly), a better implementation is to install MongoDB on the head-node and only start it whenever one logs in. Follow [this tutorial](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat-tarball/) to install via a tarball. I believe the version you want is the most recent one, with OS being RHEL and package being TGZ. And when going through the tutorial, go through the Directory Path section that allows you to use a non-default directory since we don't have sudo permissions. Test that Mongo works by using `mongod --dbpath /your/directory/for/db/ --port XXXXX`, where the dbpath option specifies where the MongoDB database will reside, and --port is specified so that we are not using the default (27017) in case anyone else might also be using that same port on the head-node. You should see the line 'Waiting for connections on port XXXXX'.

Once you have that setup, we can now start a process that runs the mongodb in the background while returning control to keyboard. In addition to the dbpath that you just made for your mongodb, create another directory where we can use Fireworks in. Then run the following, which I will break down in a moment:

```
mongod --dbpath /your/directory/for/db --nojournal --port XXXXX >> /path/to/your/fireworks/directory/db1.txt &
```
The purpose of `nojournal` is to disable the journaling feature of mongodb. This acts similarly to checkpoint files and allows for easier recovery in case the database reaches a catastrophic error. However, such checkpoint files (wiredtiger) take up gigabytes of space even for a very small database, and based on my runs I have never needed them.

After the port statement, we write the output to a log file in our created FireWorks directory, and we also turned it into a background process using `&`. This is so we have keyboard control returned to us while the mongodb is running in the background, and we can see the output as if we were running mongodb interactively in the log file. Once you exit all terminals, this command should be terminated, and once you login, you can restart it by running the same command.



### Test your connection
Head back to the HPC terminal and create a file called `my_launchpad.yaml`. Put the following in it:

```yaml
authsource: admin
host: localhost
logdir: null
name: fireworks
password: null
port: 27017 #default, but replace if different
ssl: false
ssl_ca_certs: null
ssl_certfile: null
ssl_keyfile: null
ssl_pem_passphrase: null
strm_lvl: INFO
user_indices: []
username: null
wf_user_indices: []
```

Then do the following command in the same directory:

```shell
lpad -l my_launchpad.yaml get_wflows
```
If it returns an empty array (which it should because we haven't added any workflows) rather than returning an error, then your connection is working.

### QCFW Functions
In order for my included scripts to work, you must place the functions.py from this repository to `/.local/python3.6/site-packages/qcfw`. The "qcfw" name must be exact. Or you can simply install via:

[Home](../) <code>&#124;</code> [Next](./FW2-Required-Files.html)
