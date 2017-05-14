import argparse
import csv
import os
from ode_model.utils import Species, Parameter


def prepare_system():
    args = parse_arguments()
    species = import_species(args.species, args.ode)
    parameters = import_parameters(args.parameters)
    out_dir = prepare_out(args.out)

    return args, species, parameters, out_dir


def prepare_out(out_dir):
    '''
    Description:
        This method prepares a directory according to the argument
        specified by the user, creating it if necessary.
    Input:
        out_dir - the parsed argument obtained for -out
    Returns:
        out_dir - the path to the output directory
    '''
    if not out_dir:
        out_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    return out_dir


def import_species(speciesfile, odefile):
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
        reader.next()  # skip header

        for index, row in enumerate(reader):
            s = Species()
            s.name = row[0]
            s.conc0 = float(row[1])
            s.index = int(index)
            species[s.name] = s

    with open(odefile, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        curr = ''
        for row in reader:
            if row[0] == 'Species':
                curr = row[1]
            else:
                species[curr].ode += row[0]

    return species


def import_parameters(parametersfile):
    '''
    Description:
        This method imports a csv file containing parameter information,
        according to the format described in the README file. The information
        for each parameter is stored in a dictionary. The keys of the
        dictionary are strings corresponding to the name of each parameter,
        and the value of each key is the value assigned to the parameter.
    Input:
        filename - a string containing the csv filename (including path,
            if necessary).
    Returns:
        parameters - a dictionary mapping strings to floats.
    '''

    parameters = {}
    with open(parametersfile, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        reader.next()  # Skips header

        for index, row in enumerate(reader):
            p = Parameter()
            p.name = row[0]
            p.value = float(row[1])
            p.index = int(index)
            parameters[p.name] = p

    return parameters


def parse_arguments():
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
                             for 'species.csv' in the current directory""")

    parser.add_argument("-ode", default='ode.csv', type=str,
                        help="""name of ode CSV file. Default is to look for
                             'ode.csv' in the current directory""")

    parser.add_argument("-parameters", default='parameters.csv', type=str,
                        help="""name of parameters CSV file. Default is to look
                             for 'parameters.csv' in the current directory""")

    parser.add_argument("-out", default=None, type=str,
                        help="""name of desired output directory. Default is
                             to create a folder 'output' if one does not
                             already exist in the current directory""")

    parser.add_argument("-n", default=1000,
                        help="""integer for the number of iterations of numerical
                             integration, default is 1000""")

    parser.add_argument("-t", default=3600,
                        help="""integer for the total time (seconds) modeled,
                             default is 3600""")

    return parser.parse_args()
