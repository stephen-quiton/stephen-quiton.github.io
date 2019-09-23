---
layout: default
---

# Using the WebGUI

[Previous](./FW4-Advanced-Setups.html) <code>&#124;</code> [Home](../)

This part is completely optional since you can actually check up on workflow statuses using 'lpad' commands or by looking at directly at MongoDB Atlas. But it is highly convenient (and oddly satisfying) to see the workflows complete on a website. You also don't need to do this if you're going to rely on using my database, whose WebGUI has already been setup, but you can feel free to read on to find out how I did so.

The Fireworks tutorial for the [WebGUI](https://materialsproject.github.io/fireworks/basesite_tutorial.html) does go through one way to set it up, but unfortunately, this method isn't necessarily ideal to run on the login-nodes of an HPC cluster. Instead, I ran it based on the "Running the Flask app via Python" section, dedicating a Raspberry Pi to keeping the WebGUI up and running. In principle, you could use any computer, but Raspberry Pi's are good because they're small, always running, and highly configurable. I'm using the regular Raspbian 8 (jessie) OS and VNC viewer to control it remotely.

Here's what you need:

* An installation of Python, preferably 3.4+ and with Matplotlib so that the bar plots will work.
* A short python script webgui.py that will be used to connect to the database and run the WebGUI locally
  * You can look at the bottom of the [WebGUI](https://materialsproject.github.io/fireworks/basesite_tutorial.html) tutorial and/or have a look at my example at WebGUI/
* The 'ngrok' executable obtained by signing up and logging in at the [ngrok website](https://ngrok.com/). This will be used to expose the local website to the public on a randomly generated web address.

After getting everything, cd to where webgui.py run the following to start the webserver. For this command and the next one, be sure to note the process ID in case you want to kill it later (or if you're on Raspbian, you can just look at the process manager and kill it from there):
```
nohup python3.4 webgui.py &
```
You can replace python3.4 with whatever version you have. Then run the following to expose the webserver via ngrok:
```
nohup ./ngrok http 4040 &
```
Note that 4040 matches the 'port' argument in webgui.py. Finally run the following to get your webserver address:
```
curl localhost:4041/api/tunnels
```
What results is a block of text, but in it, you should see an ngrok.io URL; that's the one you want. For some reason, doing `...localhost:4040...` when your port is 4040 does not work. Perhaps it's something to do with numbering starting with 1 or 0.

[Previous](./FW4-Advanced-Setups.html) <code>&#124;</code> [Home](../)
