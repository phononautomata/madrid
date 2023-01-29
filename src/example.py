#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 14:22:35 2021

@author: ademiguel

"""

import os

import pickle as pk

from analysis import extract_global_time_series, extract_local_time_series, \
    outline_results
from data_utils import import_population, extract_patch_integer_index, \
    build_averaged_travel_matrix, generate_metadata_string, generate_baseline_string
from model import launch_model, launch_filtered_model

import plot_example as pt

path = os.path.dirname(os.getcwd())


def perform_experiment_zero(pars):
    """
    Perform experiment zero: 
        1) Run the metapopulation model for a single set of input parameters 
        (several realizations, same initial conditions for all).
        Results stored in pickle file for further use.
        2) Summary statistics from the simulations.
        3) Collect/rearrange time series data.
        4) Plot results (time series).

    Parameters
    ----------
    pars : dict
        DESCRIPTION.

    Returns
    -------
    None.

    """

    # 1) Run the metapopulation SIR model
    results = launch_filtered_model(pars)

    # Save results into pickle
    lower_path = 'results'
    file_name = 'exp0' + generate_metadata_string(pars) + '.pickle'
    full_name = os.path.join(path, lower_path, file_name)
    output = open(full_name, 'wb')
    pk.dump(results, output)
    output.close()

    # 2) Outline results
    outline_results(results, pars)

    # 3) Collect/rearrange time series data
    global_tseries = extract_global_time_series(results, pars)

    # 4) Plot results
    pt.plot_global_dynamics(global_tseries, pars)


def main():
    # Prepare input dictionary
    pars = {}
    pars['city'] = 'MADRID'
    pars['patch_id'] = 'CENTRO'
    pars['mod_id'] = 'SIR'
    pars['mob_id'] = 'ref'
    pars['kappa'] = 1.0
    pars['seeds'] = 10
    pars['R0'] = 1.25
    pars['T_I'] = 4.5
    pars['T_E'] = 2.5
    pars['nsims'] = 10
    pars['T_MAX'] = 700
    pars['theta'] = 500
    pars['chi'] = 1.0
    pars['epsilon'] = 1.0
    pars['hold'] = True
    pars['tspan'] = 13
    pars['local'] = False
    pars['stat'] = 'avg'

    # Perform basic experiment
    perform_experiment_zero(pars)


if __name__ == "__main__":
    main()
