#!/usr/bin/env python

from ranmodel import *
import os

#Parse any arguments passed in by the user
args = parseArguments()

#Create dictionaries containing all species and all parameters specified by required CSV files
species = importSpecies('species.csv','ode.csv')
parameters = importParameters('parameters.csv')

#Define the output folder
if not args.output: output = prepareOutput(os.path.realpath(__file__),"output")
else: output = prepareOutput(os.path.realpath(__file__),args.output)

#Define parameters to sweep
#Concentration of GEF and GAP
GEF_concentrations = [0.000,0.005,0.010,0.015,0.020,0.025]
GAP_concentrations = [0.000,0.005,0.010,0.015,0.020,0.025]

#prepare cumulative figure

fig = plt.figure(figsize=(15,8))
for i in GEF_concentrations:
	ax = fig.add_subplot(2, 3, GEF_concentrations.index(i)+1)

	for j in GAP_concentrations:
		species['GEF'].conc0, species['GAP'].conc0 = i,j
		concentrations, t = runmodel(species,parameters,args)
		ax.plot(t, concentrations[:,species['SensorPi'].index])

		plt.title("GEF = %f" %i)
		plt.xlabel("Time (seconds)")
		plt.ylabel("Sensor Concentration (uM)")
	
plt.legend(["GAP = %f" %0.000,
			"GAP = %f" %0.005,
			"GAP = %f" %0.010,
			"GAP = %f" %0.015,
			"GAP = %f" %0.020,
			"GAP = %f" %0.025,
			"GAP = %f" %0.030])
fig.suptitle("Varying GAP and GEF, total time = %s seconds" %args.t,fontsize=16)
plt.tight_layout()
fig.subplots_adjust(top=.9)
fig.savefig(output + 'parameter_sweep.png')