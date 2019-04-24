#!/usr/bin/env python

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ode_modeler',
    version='0.3',
    description='ODE Model for Molecular Species',
    long_description=readme,
    author='Chris Mathy',
    author_email='chris.mathy@ucsf.edu',
    url='https://github.com/cjmathy/ode_modeler',
    license=license,
    packages=['ode_modeler']
)

