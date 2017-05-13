import argparse
import csv
import os
import numpy as np
from scipy.integrate import odeint
from ranmodel.utils import Species, Parameter


def parseArguments():
    '''
    Description:
        This method parses additional arguments passed when the script is
            called.
    Input:
        None
    Returns:
        args - a Namespace object.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-species", default='species.csv', type=str,
                        help="""name of species CSV file. Default is to look
                             for 'species.csv' in the package directory""")

    parser.add_argument("-ode", default='ode.csv', type=str,
                        help="""name of ode CSV file. Default is to look for
                             'ode.csv' in the package directory""")

    parser.add_argument("-parameters", default='parameters.csv', type=str,
                        help="""name of parameters CSV file. Default is to look
                             for 'parameters.csv' in the package directory""")

    parser.add_argument("-out", default=None, type=str,
                        help="""name of desired output directory. Default is
                             to create a folder 'output' if one does not
                             already exist in the package directory""")

    parser.add_argument("-n", default=1000,
                        help="""integer for the number of iterations of numerical
                             integration, default is 1000""")

    parser.add_argument("-t", default=3600,
                        help="""integer for the total time (seconds) modeled,
                             default is 3600""")

    parser.add_argument("-plot", default='all',
                        help="""string of the names of each species to be plotted,
                        separated by commas""")  # NEED TO ADD

    return parser.parse_args()


def importSpecies(speciesfile, odefile):
    '''
    Description:
        This method imports two csv files containing molecular species
            information, according to the formats described in the README
            file. The first file should contain initial concentration values
            for each species, while the second file should contain the ODE
            string for each species. The information for each species is
            stored as an object of the Species Class, and then stored in a
            dictionary. The keys of the dictionary are strings corresponding
            to the name of each species, and the value of each key is the
            corresponding Species object.
    Input:
        speciesfile - a string containing the csv filename (including path,
            if necessary) for the file containing Species and initial
            concentrations.
        odefile - a string containing the csv filename (including path, if
            necessary) for the file containing Species and ODE equations.
    Returns:
        species - a dictionary mapping strings to Species objects.
    '''
    species = {}
    with open(speciesfile, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        reader.next()  # This skips the CSV row containing the column headings
        index = 0
        for row in reader:
            s = Species()
            s.name = row[0]
            s.conc0 = float(row[1])
            s.index = int(index)
            species[s.name] = s
            index += 1
    with open(odefile, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        curr = ''
        for row in reader:
            if row[0] == 'Species': curr = row[1]
            else: species[curr].ode += row[0]
    return species


def importParameters(parametersfile):
    '''
    Description:
        This method imports a csv file containing parameter information, according to the format described in the README file. The information for each parameter is stored in a dictionary. The keys of the dictionary are strings corresponding to the name of each parameter, and the value of each key is the value assigned to the parameter.
    Input:
        filename - a string containing the csv filename (including path, if necessary).
    Returns:
        parameters - a dictionary mapping strings to floats.
    '''

    parameters = {}
    with open(parametersfile, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        reader.next() #This skips the CSV row containing the column headings
        index = 0
        for row in reader:
            p = Parameter()
            p.name = row[0]
            p.value = float(row[1])
            p.index = int(index)
            parameters[p.name] = p
            index += 1
    return parameters


def prepareOutput(path, outputdir):
    '''
    Description:
        This method takes in the path of the target directory and creates an output directory named by "outputdir" if one does not already exist.
    Inputs:
        path - the path to the directory which will contain the output folder
        outputdir - the name of the output directory (to be created, if it does not already exist)
    Returns:
        dir - the path to the output directory which will contain saved plots.
    '''
    dir = os.path.dirname(path) + '/' + outputdir + '/'
    if not os.path.exists(dir): os.makedirs(dir)
    return dir


def runmodel(species,parameters,sysargs):
    '''
    Description:
        This method prepares the system and calls the odeint method, which performs the ode integration over the specified time course. The odeint method requires the definition of an odeSystem function, which computes the derivative of the function at a given timepoint.
    Inputs:
        species - a dictionary mapping strings to Species objects.
        parameters - a dictionary mapping strings to floats.
        sysargs - a Namespace object corresponding to parsed command line inputs (see the parseArguments() method)
    Returns:
        concentrations - a numpy array with dimensions n_species x n_timepoints
        t - the numpy array with dimensions 1 x n_timepoints (useful for plotting concentration vs. time)
    '''
    # Prepare initial concentration and time vectors for odeint
    c0 = initializeConcentrations(species)
    t = np.linspace(0, int(sysargs.t), int(sysargs.n))

    #Solve the system of Ordinary Differential Equations, returning a 2-dimensional array. Cell i,j of concentrations contains the concentration value of Species i at timepoint j.
    concentrations = odeint(odeSystem,
                            c0,
                            t,
                            args=(species, parameters))

    return concentrations, t


def initializeConcentrations(species):
    '''
    Description:
        This method takes in a dictionary of species objects and creates a numpy array containing the initial concentrations of each species. The array is ordered according to the indexes unique to each Species object, which correspond to the ordering of the csv file.
    Input:
        species - a dictionary of Species objects.
    Returns:
        c0 - a numpy array of floats
    '''
    c0 = np.empty(len(species))
    for s in species:
        c0[species[s].index] = species[s].conc0
    return c0


def odeSystem(y,t,species,parameters):
    '''
    Description:
        This method prepares a system of first order ODEs for odeint. It computes the derivative of y (the vector of molecular species) at t. First, a variable is created for each Species and set to the current value found in y. Then, a variable is created for each Parameter, and set to its corresponding value. Finally, the derivate expressions for each species are evaluated according to these variables, and stored in the list dydt.
    Inputs:
        y - a numpy ndarray of floats (representing concentrations).
        t - a numpy ndarray of floats (representing timepoints). t is not explicitly called in the odeSystem method, but is required by odeint.
        species - a dictionary mapping strings to Species objects.
        parameters - a dictionary mapping strings to Parameter objects.
    Returns:
        dydt - a list of floats representing rates of change in concentration.
    '''
    for s in species:
        exec("%s = %.100f" % (s,y[int(species[s].index)]))
    for p in parameters:
        exec("%s = %.100f" % (p,parameters[p].value))
    dydt = [None]*len(species)
    for s in species:
        dydt[int(species[s].index)] = eval(species[s].ode)
    return dydt
