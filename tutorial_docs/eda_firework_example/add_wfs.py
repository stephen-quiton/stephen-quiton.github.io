#!/usr/bin/env python
from fireworks import LaunchPad, Firework, Workflow, PyTask
import glob

launchpad = LaunchPad(
    host = 'localhost',
    port = 27017, # REPLACE
    authsource = 'admin',
    name = 'fireworks',
    password = None, 
    ssl = False,
    username = None 
) 

for inp in glob.glob('eda*.inp'): 
    label = inp[0:-4]
    t0 = PyTask(
        func='qcfw.functions.run_QChem',
        kwargs={'label':label},
        outputs = ['output_encoding']
        )
    fw0 = Firework([t0], spec={'_priority': 1}, name=label,fw_id=1)    
    wf = Workflow ([fw0],name=label)
    launchpad.add_wf(wf)


