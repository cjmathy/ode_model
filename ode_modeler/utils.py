class Species():
    '''
    This class defines a Species object, representing one molecular species
    present in the model.
    Attributes:
        name:
            string - the name of the Species used in the ODE equations.
        conc0:
            float - the initial concentration of the species.
        ode:
            string - the right hand side of the first-order differential
            equation for the species. For example, if the equation governing
            the rate of change of species A is <d[A]/dt = k*B + C>, then the
            ode string should be "k*B+C" and be an attribute of Species "A".
            Note that the species and parameter names in the ode string must
            match the names listed in the csv file inputs.
        index:
            int - the index number of the Species. This allows for order to
            be recorded while storing Species in a dictionary. Keeping track
            of the order is necessary for scipy.integrate.odeint, in which
            the y vector must be kept in the correct order for each iteration.
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
    This class defines a Query object, representing one set of parameters
    to be assessed with the model.
    Attributes:
        name:
            string - name of the query

        parameters:
            dict - mapping of parameter names (strings) to values (floats)

        concentrations:
            numpy array - array of shape (ttot, n_sp), where n_sp is the
            number of species in the system. Cell (i,j) contains the
            concentration value for species j at timepoint i.

    '''
    def __init__(self):
        ''' Constructor for this class. '''
        self.name = ''
        self.parameters = {}
        self.concentrations = None

    def __repr__(self):
        return self.name
