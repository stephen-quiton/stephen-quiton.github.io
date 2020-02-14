from pymatgen.io.qchem.outputs import QCOutput
import glob, csv

num_outputs= len(glob.glob("eda*.out"))

energy = [None]*num_outputs
prp = [None]*num_outputs
frz = [None]*num_outputs
pol = [None]*num_outputs
vct = [None]*num_outputs
inter = [None]*num_outputs

elec = [None]*num_outputs
pauli = [None]*num_outputs
disp = [None]*num_outputs

for file in glob.glob("eda*.out"):
    output = QCOutput(filename = file)
    i_string= file.split('.')[0][3:len(file)]
    i = int(i_string)
    energy[i-1] = output.data['final_energy']

for file in glob.glob("eda*.out"):
    output = QCOutput(filename = file)
    i_string= file.split('.')[0][3:len(file)]
    i = int(i_string)

    prp[i-1] = output.data['EDA_data']['E_prp']
    frz[i-1] = output.data['EDA_data']['E_frz']
    pol[i-1] = output.data['EDA_data']['E_pol']
    vct[i-1] = output.data['EDA_data']['E_vct']
    inter[i-1] = output.data['EDA_data']['E_int']

    elec[i-1] = output.data['EDA_data']['E_elec']
    pauli[i-1] = output.data['EDA_data']['E_pauli']
    disp[i-1] = output.data['EDA_data']['E_disp']

with open('EDA_data.csv', mode='w') as csv_file:
    fieldnames = ['Filename','Energy','E_prp','E_frz','E_pol','E_vct','E_int','E_elec','E_pauli','E_disp']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for n in range(num_outputs):
        writer.writerow(
            {
                'Filename':'eda'+str(n+1)+'.out',
                'E_Energy':energy[n],
                'E_prp':prp[n],
                'E_frz':frz[n],
                'E_pol':pol[n],
                'E_vct':vct[n],
                'E_int':inter[n],

                'E_elec':elec[n],
                'E_pauli':pauli[n],
                'E_disp':disp[n]
            }
        )
