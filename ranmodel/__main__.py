from ranmodel import *
import os


#*****TO PULSE, JUST RUN SYSTEM TWICE, WITH LAST CONC VALUES BECOMING CONC0 OF SECOND RUN!

#Parse any arguments passed in by the user
sysargs = parseArguments()

#Create dictionaries containing all species and all parameters specified by required CSV files
# species = importSpecies('species.csv','ode.csv')
# parameters = importParameters('parameters.csv')

#Create dictionaries containing all species and all parameters specified by required CSV files
species = importSpecies(sysargs.species,sysargs.ode)
parameters = importParameters(sysargs.parameters)

#Define the output folder
if not sysargs.out: output = prepareOutput(os.path.dirname(__file__),"output")
else: output = prepareOutput(os.path.dirname(__file__),sysargs.out)


#----------SINGLE RUN----------
#Run model
# concentrations, t = runmodel(species,parameters,sysargs)

# #Produce plots of all concentrations, according to user provided plotting instructions
# plot_all_species_separate_plots(concentrations,t,species,sysargs,output)
# plot_ran_ratios(concentrations,t,species,sysargs,output)
# plot_all_species_one_plot(concentrations,t,species,sysargs,output)


import numpy as np


#PE = (Km,Kcat)
PE1 = (1.353,0.044)
PE11 = (3.704,0.036)
PE13 = (2.631,0.007)
PE18 = (0.783,0.045)

proteins = [PE1,PE11,PE13,PE18]
protein_names = ['WT','T34G','T34Q','R108Y']


# for protein in proteins:
# 	name = protein_names[proteins.index(protein)]
# 	parameters['Km_GAP'].value = protein[0]
# 	parameters['kcat_GAP'].value = protein[1]
# 	fig = plt.figure(figsize=(15,8))
# 	concentrations, t = runmodel(species,parameters,sysargs)
# 	plot_ran_ratios(concentrations,t,species,sysargs,output,fig)
# 	fig.suptitle("Ran Species Ratios, %s" %name)
# 	plt.tight_layout()
# 	fig.subplots_adjust(top=.9)
# 	fig.savefig(output + '%s.png' %name)

for protein in proteins:
	name = protein_names[proteins.index(protein)]
	parameters['Km_GAP'].value = protein[0]
	parameters['kcat_GAP'].value = protein[1]
	concentrations, t = runmodel(species,parameters,sysargs)

	nucRanGTP = concentrations[t.shape[0]-1,species['nucRanGTP'].index]
	nucRanGDP = concentrations[t.shape[0]-1,species['nucRanGDP'].index]
	cytoRanGTP = concentrations[t.shape[0]-1,species['cytoRanGTP'].index]
	cytoRanGDP = concentrations[t.shape[0]-1,species['cytoRanGDP'].index]

	labels = ['nucRanGTP/nucRanGDP','cytoRanGTP/cytoRanGDP','nucRanGTP/cytoRanGTP','nucRanGDP/cytoRanGDP']
	ratios = [nucRanGTP/nucRanGDP,cytoRanGTP/cytoRanGDP,nucRanGTP/cytoRanGTP,nucRanGDP/cytoRanGDP]

	plt.plot(labels,ratios)
	plt.show()




	fig.suptitle("Ran Species Ratios, %s" %name)
	plt.tight_layout()
	fig.subplots_adjust(top=.9)
	fig.savefig(output + '%s.png' %name)


# for parameter in parameters:
# 	k = parameters[parameter].value

# 	fig = plt.figure(figsize=(15,8))

# 	for delta in np.logspace(-1,1,11):
# 		parameters[parameter].value = k*delta
# 		concentrations, t = runmodel(species,parameters,sysargs)
# 		plot_ran_ratios(concentrations,t,species,sysargs,output,fig)

# 	fig.suptitle("Ran Species, varying %s" %parameter)
# 	plt.tight_layout()
# 	fig.subplots_adjust(top=.9)
# 	fig.savefig(output + 'ran_species_varying_%s.png' %parameter)

# 	parameters[parameter].value = k




# y[t.size,species['nucRanGTP'].index]/y[:,species['nucRanGDP'].index
