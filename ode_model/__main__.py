import ode_model.io as io
from ode_model.runmodel import run
import ode_model.plot as plot

# read in user arguments
kwargs = io.parse_arguments()

# build system
species = io.import_species(**kwargs)
queries = io.import_queries(**kwargs)

# run for each query
for query in queries:
    parameters = query.parameters
    query.concentrations, query.t = run(species, parameters, **kwargs)

io.final_conc_table(species, queries, **kwargs)
plot.plot_all_queries(species, queries, **kwargs)
plot.plot_each_query(species, queries, **kwargs)
