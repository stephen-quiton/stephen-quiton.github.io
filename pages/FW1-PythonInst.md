---
layout: default
---

## Installing FireWorks and Setting up MongoDB

[Home](../) | [Next](./FW2-Required-Files.html)

### FireWorks

Installing python packages on HPC is [not necessarily the same](https://hpcc.usc.edu/support/documentation/python/) as if you were to do the same with your own machine. This is because the command `pip` usually goes to a directory guarded by sudo permissions, which we don't have. Thus, the commands we need to use are: 

```shell
source /usr/usc/python/3.6.0/setup.sh
pip install FireWorks --user
```

I highly recommend you place the first line in your ~/.bashrc so python is setup when you enter the shell. With the `--user` option, the FireWorks python package should be installed to ~/.local. You can keep .local where it is if you'd like, but I've decided to make ~/.local a soft-link to a directory with more quota space so I don't have to be concerned with storage.

To test if FireWorks is installed correctly, restart your terminal and run the command `lpad`. If it returns with a list of options to use with `lpad`, you're ready to go

### MongoDB

FireWorks can be used with any remote database, but the one that has worked most reliably for me thus far is [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). Make an account there and select the free options and using any platform (I'm using Azure). 

When you setting it up, you should have come across the list of IPs to whitelist (click on "Network Access" on the sidebar). For now, the only IP address we want to add is HPC's login node, which you can do by adding `10.125.0.0/0`. As a last resort, if you later come to connection problems, you can allow access from all IPs (add `0.0.0.0/0`), but this is generally not recommended because at that point, your database can be modified from anywhere. 

Something else you may have come across is creating user-password combo to access the database ("Database Access" on the sidebar). You only need one, and make sure its user privileges is set to "Atlas admin." 

Finally, when you click "Clusters" on the sidebar, you should be able to see three different hostnames, with one being designated the 'Primary' cluster. Click on that one, and you should be able to get the full host name in this format:

```
cluster0-shard-00-0x-abcdef.azure.mongodb.net:27017
```

The `x` could be any number depending on which one was selected as primary. Everything before the colon is the hostname, and the 5-digit to the right is the port. Keep this info handy later on. 

Also keep in mind that the primary cluster changes once in a while, so make sure that when you're doing a task that involves connecting to the launchpad that you're connecting to the _primary_ cluster. If you don't you may get a python exception called "Not_master" or something to that effect.


### Test your connection
Head back to the HPC terminal and create a file called `my_launchpad.yaml`. Put the following in it:

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

Replace the appropriate values (host, name, username, password) as necessary for your case. Then do the following command in the same directory:

```shell
lpad -l my_launchpad.yaml get_wflows
```
The `-l` optiIf it returns an empty array (which it should because we haven't added any workflows) rather than returning an error, then your connection is working.

[Home](../) | [Next](./FW2-Required-Files.html)