---
layout: default
---

# Using the WebGUI

[Previous](./FW4-Advanced-Setups.html) <code>&#124;</code> [Home](../)

This part is completely optional since you can actually check up on workflow statuses using 'lpad' commands or by looking at directly at MongoDB Atlas. But it is highly recommended as it is convenient (and oddly satisfying) to see the workflows complete on a website.

The Fireworks tutorial for the [WebGUI](https://materialsproject.github.io/fireworks/basesite_tutorial.html) does go through one way to set it up, but unfortunately, this method isn't necessarily ideal to run on the login-nodes of an HPC cluster, as it is difficult to use the shell-based terminal, and as far as know, there are no X-11 browsers. Instead, I ran it based on the "Running the Flask app via Python" section, broadcasting the data in our mongodb to a specific port, and then portforwarding from our laptops to that specific port.

Here's what you need:

* An installation of Python, preferably 3.4+ and with Matplotlib so that the bar plots will work.
* A short python script webgui.py that will be used to connect to the database and run the WebGUI locally. An example is provided below:

```python
from fireworks import LaunchPad
from fireworks.flask_site.app import app

app.lp = LaunchPad(
    host = 'localhost',
    port = XXXXX,
    authsource = 'admin',
    name = 'fireworks',
    password = None,
    ssl = False,
    username = None)  # change the LaunchPad info if needed

app.run(port=YYYY,debug=True)
```
Your launchpad port XXXXX should match your MongoDB port, and YYYY, which is the headnode port you're running the WebGUI on, can be whatever you want but keep it handy for later on.

After getting everything, login to either USC headnode 2 or 3 using the following, where YYYY is the port we specified in webgui.py, and XXXX is the port on your laptop where you'd like to access the WebGUI via a browser, like 8080:
```
ssh -L ZZZZ:localhost:YYYY username@hpc-loginX.usc.edu
```
Then place webgui.py in some directory on the headnode run the following to start the webserver
```
python /location/of/webgui.py &> /some/log.txt &
```
You can replace python3.4 with whatever version you have. As you can see, we incorporate writing the output to a log file so that we can have this script running in the background. Now on any browser, type `localhost:ZZZZ`, and you should see a webpage similar to the one shown on the image of the [FireWorks WebGUI tutorial](https://materialsproject.github.io/fireworks/basesite_tutorial.html).

And remember that you can place any commands in the bashrc that you find repetitive, so that you don't have to run them every time you login.

### Exposing the website to the public
The one disadvantage of the above method is that you must be logged in to a terminal in order to see the webpage. If you wanted to see it even when logged out, you can follow this [deprecated page](./FW5-WebGUI_deprecated.html), but it is convoluted and, in my opinion, not worth the effort.

[Previous](./FW4-Advanced-Setups.html) <code>&#124;</code> [Home](../)
