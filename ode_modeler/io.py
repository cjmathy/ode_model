import argparse
import csv
import os
from ode_modeler.utils import Species, Query


def import_species(species_file, ode_file, **kwargs):
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
        species_file - a string containing the csv filename (including path,
            if necessary) for the file containing Species and initial
            concentrations.
        ode_file - a string containing the csv filename (including path, if
            necessary) for the file containing Species and ODE equations.
    Returns:
        species - a dictionary mapping strings to Species objects.
    '''

    species = {}
    with open(species_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip header

        for index, row in enumerate(reader):
            s = Species()
            s.name = row[0]
            s.conc0 = float(row[1])
            s.index = int(index)
            species[s.name] = s

    with open(ode_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        curr = ''
        for row in reader:
            if row[0] == 'Species':
                curr = row[1]
            else:
                species[curr].ode += row[0]

    return species


def import_queries(queries_file, **kwargs):
    '''
    Description:
        This method imports a csv file containing parameter information for
        each query, according to the format described in the README file.
        A Query object describes one set of parameters for a model run. The
        parameters read in from the query file are stored in a parameters
        dictionary, an attribute of the Query object. The keys of the
        dictionary are strings corresponding to the name of each parameter,
        and the value of each key is the value assigned to the parameter.
    Input:
        queries_file - a string containing the csv filename (including path,
            if necessary) for the file containing parameter information for
            all queries.
    Returns:
        queries - a list of query objects.
    '''

    queries = []
    with open(queries_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        param_list = next(reader)[1:]

        for i, row in enumerate(reader):
            q = Query()
            q.name = row[0]
            for j, param in enumerate(row[1:]):
                param_name = param_list[j]
                q.parameters[param_name] = float(param)
            queries.append(q)

    return queries


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


def final_conc_table(species, queries, out_dir, **kwargs):
    '''
    Description:
        This method prepares a CSV file listing the final concentrations for
        all species, for all queries.
    Input:
        species - a dictionary mapping strings to Species objects.
        queries - a list of query objects.
        out_dir - the path to the output directory
    Returns:
        out_dir - the path to the output directory
    '''

    species_list = [None]*len(species)
    for sp in species:
        species_list[species[sp].index] = sp

    with open(os.path.join(out_dir, 'final_conc.csv'), 'w') as f:
        for query in queries:
            f.write(',{}'.format(query.name))
        f.write('\n')
        for sp in species_list:
            f.write(sp)
            for j, query in enumerate(queries):
                f.write(",{}".format(
                    query.concentrations[0][-1, species[sp].index]))
            f.write('\n')
    return


def parse_arguments():
    '''
    Description:
        This method parses additional arguments passed when the script is
        called. It then prepares a kwargs dictionary to be used by the
        package.
    Input:
        None
    Returns:
        kwargs - a dictionary containing package settings, set by user.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-species", default='species.csv', type=str,
                        help="""name of species CSV file. Default is to look
                             for 'species.csv' in the current directory""")

    parser.add_argument("-ode", default='ode.csv', type=str,
                        help="""name of ode CSV file. Default is to look for
                             'ode.csv' in the current directory""")

    parser.add_argument("-queries", default='queries.csv', type=str,
                        help="""name of queries CSV file. Default is to look
                             for 'queries.csv' in the current directory""")

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

    parser.add_argument("-plot_species", default="all",
                        help="""list of species to include in the plotting.
                             species names must match those in species CSV
                             file. format as one string, comma-separated.
                             default is to plot all species""")

    parser.add_argument("-out_format", default="pdf_one", type=str,
                        choices=set(("pdf_mult", "pdf_one", "png")),
                        help="""output format of figures. choice of
                             multiple PDFs, one collated PDF, or multiple
                             PNGs""")

    args = parser.parse_args()

    kwargs = {
        'species_file': args.species,
        'ode_file': args.ode,
        'queries_file': args.queries,
        'out_dir': prepare_out(args.out),
        'n_iter': int(args.n),
        'ttot': int(args.t),
        'plot_species': args.plot_species.split(","),
        'out_format': args.out_format
    }

    return kwargs
