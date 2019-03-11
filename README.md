#ODE Model

This project implements a numerical integrator for solving systems of ordinary differential equations describing molecular species. The project is written in Python 3.6.

## Usage

To use the package, first run

```
conda install --yes --file requirements.txt
```

to install all the dependencies in `requirements.txt`. Then the package's
main function (located in `ode_model/__main__.py`) can be run as follows:

```
python -m ode_modeler
```

System parameters are set using CSV files. Example CSV files can be found in the examples folder, along with an explanatory text file.

A number of user options are provided, set from the command line. Please see the parse_arguments method in ode_model/io.py. Importantly, -t is used to set the length of simulation. Users are encouraged to test different simulation lengths as molecular systems can operate on vastly different timescales.

## Contact

Feel free to contact at the following email addresses:
chris.mathy@ucsf.edu
cjmathy@gmail.com
