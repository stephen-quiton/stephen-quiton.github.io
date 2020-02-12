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

label = input[0:-4]
t0 = PyTask(
    func='qcfw.functions.run_QChem',
    kwargs={'label':label},
    outputs = ['output_encoding']
    )
fw0 = Firework([t0], spec={'_priority': 1}, name=label,fw_id=1)    
wf = Workflow ([fw0],name=label)
launchpad.add_wf(wf)