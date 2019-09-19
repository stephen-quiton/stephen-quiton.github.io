---
layout: default
---

## Installing FireWorks and Setting up MongoDB


### FireWorks

Installing python packages on HPC is [not necessarily the same](https://hpcc.usc.edu/support/documentation/python/) as if you were to do the same with your own machine. This is because the command `pip` usually goes to a directory guarded by sudo permissions, which we don't have. Thus, the commands we need to use is: 

```
source /usr/usc/python/3.6.0/setup.sh
pip install FireWorks --user
```

I highly recommend you place the first line in your ~/.bashrc so python is setup when you enter the shell. With the `--user` option, the FireWorks python package should be installed to ~/.local. You can keep .local where it is if you'd like, but I've decided to make ~/.local a soft-link to a directory with more quota space so I don't have to be concerned with storage.

### MongoDB

FireWorks can be used with any remote database, but the one that has worked most reliable for me thus far is [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). Make an account there and select the free options and using any platform (I'm using Azure). When you set everything up and click "Clusters" on the right sidebar, you should be able to see three different hostnames, with one being designated the 'Primary' cluster. Click on that one, and you should be able to get the full host name in this format:

```
cluster0-shard-00-0x-abcdef.azure.mongodb.net:27017
```

The `x` could be any number depending on which one was selected as primary. Everything before the colon is the hostname, and the 5-digit to the right is the port. Keep this info handy later on. 



[back](../)
