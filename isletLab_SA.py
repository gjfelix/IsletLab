import numpy as np
import re
import glob



def generar_SA_opt_code()

def buscar_global_contacts(mainfolder):
	return sorted(glob.glob(mainfolder+'/**/*_global_contacts.txt', recursive = True))


def contar_celulas(file):
	data = np.loadtxt(file)
	return len(data)

input_folder = '/home/gerardo/Documents/isletsnetworks-main'
output_folder = '/home/gerardo/Documents/kuramoto_islets/repository/G_baja/'
filelist = buscar_global_contacts(input_folder)

sourcefile = '/home/gerardo/Documents/kuramoto_islets/Human/H02/kuramoto_islets.cu'

# abro archivo a modificar
fsource = open(sourcefile, "r")
# leo archivo original
lines = fsource.readlines()

for file in filelist[:]:
	# contar numero de celulas en cada islote
	ncells = contar_celulas(file)
	
	# nombre de islote
	id_islote = file[-23:-20]

	# nombre de archivo de salida
	fout = output_folder + id_islote + "_kuramoto_islets_BajaG.cu"
	fsalida = open(fout, "w")
	#print(fout)
	
	lines[20] = "#define totalCelulas " + str(ncells) +"\n"
	lines[139] = 'fp = fopen("' + id_islote + '_global_contacts_adjMat_BajaG.txt" ,"r");\n' 
	lines[247] = 'fp = fopen("' + id_islote + '_global_contacts_Kmat_BajaG.txt", "r");\n'
	lines[333] = 'FILE *salidaAngulosIslote = fopen("'+id_islote+'_AngulosIslote_BajaG.data", "w");\n'

	for line in lines:
		fsalida.write(line)
	fsalida.close()



fsource.close()

