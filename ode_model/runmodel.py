import numpy as np
from scipy.integrate import odeint


def run(species, parameters, args):
    '''
    Description:
        This method prepares the system and calls the odeint method, which
        performs the ode integration over the specified time course. The
        odeint method requires the definition of an ode_ststem method,
        which computes the derivative of the function at a given timepoint.
    Inputs:
        species - a dictionary mapping strings to Species objects.
        parameters - a dictionary mapping strings to floats.
        args - a Namespace object corresponding to parsed command line
            inputs (see the parseArguments() method)
    Returns:
        concentrations - a numpy array with dimensions n_species x n_timepoints
        t - the numpy array with dimensions 1 x n_timepoints (useful for
            plotting concentration vs. time)
    '''

    # Prepare initial concentration and time vectors for odeint
    c0 = initialize_concentrations(species)
    t = np.linspace(0, int(args.t), int(args.n))

    # Solve system of ODEs. Cell i,j of concentrations contains the
    # concentration value of Species i at timepoint j.
    concentrations = odeint(ode_system,
                            c0,
                            t,
                            args=(species, parameters))

    return concentrations, t


def initialize_concentrations(species):
    '''
    Description:
        This method takes in a dictionary of species objects and creates a
        numpy array containing the initial concentrations of each species.
        The array is ordered according to the indexes unique to each Species
        object, which correspond to the ordering of the csv file.
    Input:
        species - a dictionary of Species objects.
    Returns:
        c0 - a numpy array of floats
    '''
    c0 = np.empty(len(species))
    for s in species:
        c0[species[s].index] = species[s].conc0
    return c0


def ode_system(y, t, species, parameters):
    '''
    Description:
        This method prepares a system of first order ODEs for odeint. It
        computes the derivative of y (the vector of molecular species) at t.
        First, a variable is created for each Species and set to the current
        value found in y. Then, a variable is created for each Parameter, and
        set to its corresponding value. Finally, the derivate expressions for
        each species are evaluated according to these variables, and stored in
        the list dydt.
    Inputs:
        y - a numpy ndarray of floats (representing concentrations).
        t - a numpy ndarray of floats (representing timepoints). t is not
            explicitly called in ode_system, but is required by odeint.
        species - a dictionary mapping strings to Species objects.
        parameters - a dictionary mapping strings to Parameter objects.
    Returns:
        dydt - a list of floats representing rates of change in concentration.
    '''
    for s in species:
        exec("%s = %.100f" % (s, y[int(species[s].index)]))
    for p in parameters:
        exec("%s = %.100f" % (p, parameters[p].value))
    dydt = [None]*len(species)
    for s in species:
        dydt[int(species[s].index)] = eval(species[s].ode)
    return dydt
