class Species():
    '''
    This class defines a Species object, representing one molecular species
    present in the model.
    Attributes:
        name:
            A string corresponding to the name of the Species used in the
            ODE equations.
        conc0:
            A float corresponding to the initial concentration of the species.
        ode:
            A string containing the right hand side of the first-order
            differential equation for the species. For example, if the
            equation governing the rate of change of species A is <d[A]/dt =
            k*B + C>, then the ode string should be "k*B+C" and be an
            attribute of Species "A". Note that the species and parameter
            names in the ode string must match the names listed in the csv
            files 'species.csv' and 'parameters.csv'.
        index:
            An integer representing the index number of the Species. This
            allows for order to be recorded while storing Species in a
            dictionary. Keeping track of the order is necessary for
            scipy.integrate.odeint, in which the y vector must be kept in
            the correct order for each iteration.
    '''
    def __init__(self):
        ''' Constructor for this class. '''
        self.name = ''
        self.conc0 = -1
        self.ode = ''
        self.index = -1

    def __repr__(self):
        return self.name


class Query():
    '''
    This class defines a Query object, representing one molecule being studied,
    with a unique set of associated parameters.
    Attributes:
        name:
            string: name of the molecule being queried

        parameters:
            dict: maps parameter names (strings) to values (floats)

    '''
    def __init__(self):
        ''' Constructor for this class. '''
        self.name = ''
        self.parameters = {}
        self.concentrations = None

    def __repr__(self):
        return self.name
