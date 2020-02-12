from fireworks import Firework, Workflow, PyTask, FWorker, LaunchPad

launchpad = LaunchPad(
    host = 'localhost',
    port = 27017,#default, replace with yours
    authsource = 'admin',
    name = 'fireworks',
    password = None,
    ssl = False,
    username = None
)

freqRem ={
    'basis':'6-31G',
    'job_type':'freq',
    'exchange':'b3lyp',
    'scf_convergence':'8',
    'sym_ignore':'true',
}

opt_label = 'qchem_opt' #replace with your qchem file name w/o extension
freq_label = 'qchem_freq' #replace with name of frequency file
label = 'qchem' #name of the workflow


#Construct Firework 1: Optimization
t0 = PyTask(
    func='qcfw.functions.run_QChem',
    kwargs={'label':opt_label},
    outputs = ['output_encoding'],
    )
optFW = Firework([t0], spec={'_priority': 1}, name=opt_label,fw_id=1)

#Construct Firework 2: Frequency
t1 = PyTask(
    func='qcfw.functions.run_QChem',
    args=[freq_label],
    kwargs={'rem':freqRem},
    stored_data_varname='parsed_data',
    inputs = ['output_encoding'],
    )        
freqFW = Firework([t1], spec={'_priority': 1}, name=freq_label,fw_id=2)

wf = Workflow ([optFW,freqFW],{1:[2]},name=label)
launchpad.add_wf(wf)