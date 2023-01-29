#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 21:08:14 2021

@author: ademiguel

This file hosts the analysis functions for the generated data through the
simulations of the PERIMETRAL project's model. It also includes functions for 
the analysis of mobility data independently of the epidemic model.

The model used is a metapopulation SIR epidemic model with real mobility
data that implements perimeter lockdowns.  

Disclaimer: this code allowed to obtain the result for the manuscript and 
consequently has been checked. It is now being offered publicly but there 
is still a lot of work to do regarding code organization, documentation, 
refactoring, error handling, and so on.

"""

import os

import numpy as np
import pandas as pd
import pickle as pk
import datetime

import data_utils as du


def extract_global_time_series(results, pars):
    """ 
    Obtain the time evolution of a series of relevant observables in the
    metapopulation system at the global level.

    Parameters
    ----------
    results : TYPE
        DESCRIPTION.
    pars : TYPE
        DESCRIPTION.

    Returns
    -------
    global_st_dict : TYPE
        DESCRIPTION.

    """
    
    # Unpack results
    pop_spht = results['pops']
    risk_spt = results['risk'] 
    Rt_spt = results['Rt']
    Rt_gt = results['Rt_g']
    #time_span = 14

    # Obtain global-level time series
    global_s_st = np.sum(pop_spht[:,:,0], axis=1)
    global_risk_st = np.sum(risk_spt, axis=1)
    global_Rt_st = np.sum(Rt_spt, axis=1)
 
    if pars['mod_id'] == 'SIR':
        global_i_st = np.sum(pop_spht[:,:,1], axis=1)
        global_r_st = np.sum(pop_spht[:,:,2], axis=1)
        N = global_s_st + global_i_st + global_r_st
        #global_CIR_st = compute_CIR(global_new_st, global_s_st, N, time_span)
        global_st_dict = {'S': global_s_st, 'I': global_i_st, 'R': global_r_st, 
                          'N': N, 'risk': global_risk_st, 'Rt': global_Rt_st,
                          'Rt_g': Rt_gt}
    elif pars['mod_id'] == 'SEIR':
        global_e_st = np.sum(pop_spht[:,:,1], axis=1)
        global_i_st = np.sum(pop_spht[:,:,2], axis=1)
        global_r_st = np.sum(pop_spht[:,:,3], axis=1)
        N = global_s_st + global_e_st + global_i_st + global_r_st
        #global_CIR_st = compute_CIR(global_new_st, global_s_st, N, time_span)
        global_st_dict = {'S': global_s_st, 'E': global_e_st, 'I': global_i_st,
                          'R': global_r_st, 'N': N, 'risk': global_risk_st,
                          'Rt': global_Rt_st}

    return global_st_dict


def extract_local_time_series(results, pars):
    """ 
    Obtain the time evolution of a series of relevant observables in the
    metapopulation system at the district level.

    Parameters
    ----------
    results : TYPE
        DESCRIPTION.
    pars : TYPE
        DESCRIPTION.

    Returns
    -------
    local_st_dict : TYPE
        DESCRIPTION.

    """
    
    # Unpack inputs
    pop_spht = results['pops']
    cir_spt = results['cir']
    imports_spt = results['imports']
    exports_spt = results['exports']
    invaded_spt = results['invaded']
    newcases_spt = results['newcases']
    decays_spt = results['decays']
    risk_spt = results['risk'] 
    R0_spt = results['R0']
    Rt_spt = results['Rt']
    city_name = pars['city']
    mod_id = pars['mod_id']
    
    # Get name of the districts
    patch_name_list = du.get_patch_name_list(city_name)
    
    local_st_dict = {}
    
    V = len(pop_spht[0])

    for patch in range(0, V):

        patch_name = patch_name_list[patch]

        # Store all simulations in dictionary
        s_st = pop_spht[:,patch,0]
        cir_st = cir_spt[:,patch]
        imports_st = imports_spt[:,patch]
        exports_st = exports_spt[:,patch]
        invaded_st = invaded_spt[:,patch]
        newcases_st = newcases_spt[:,patch]
        decays_st = decays_spt[:,patch]
        risk_st = risk_spt[:,patch]
        R0_st = R0_spt[:,patch]
        Rt_st = Rt_spt[:,patch]
        
        if mod_id == 'SIR':
            
            i_st = pop_spht[:,patch,1]
            r_st = pop_spht[:,patch,2]
            n_st = s_st + i_st + r_st

            local_st_dict[patch_name] = {'S': s_st, 'I': i_st, 'R': r_st,
                                         'N': n_st, 'imp': imports_st,
                                         'exp': exports_st, 'inv': invaded_st,
                                         'new': newcases_st, 'dec': decays_st,
                                         'risk': risk_st, 'R0': R0_st,
                                         'Rt': Rt_st, 'cir': cir_st}

        elif mod_id == 'SEIR':
            
            e_st = pop_spht[:,patch,1]
            i_st = pop_spht[:,patch,2]
            r_st = pop_spht[:,patch,3]
            n_st = s_st + e_st + i_st + r_st

            local_st_dict[patch_name] = {'S': s_st, 'E': e_st, 'I': i_st,
                                         'R': r_st, 'N': n_st, 
                                         'imp': imports_st, 'exp': exports_st, 
                                         'inv': invaded_st, 'new': newcases_st, 
                                         'dec': decays_st, 'risk': risk_st, 
                                         'R0': R0_st, 'Rt': Rt_st, 
                                         'cir': cir_st}

    return local_st_dict


def extract_time_series_statistics(obs_st):
    """ 
    Compute relevant statistics for a given time series of an observable 
    measured for several simulations.
    
    Parameters
    ----------
    obs_st : TYPE
        DESCRIPTION.
    obs_pars : TYPE
        DESCRIPTION.

    Returns
    -------
    tss_dict : TYPE
        DESCRIPTION.

    """

    # Compute average trajectory
    obs_avg_t = np.mean(obs_st, axis=0)
    # Compute standard deviation
    obs_std_t = np.std(obs_st, axis=0)
    # Compute 95% confidence interval
    z = 1.96
    nsims = len(obs_st)
    obs_l95_t = obs_avg_t - (z * obs_std_t / nsims)
    obs_u95_t = obs_avg_t + (z * obs_std_t / nsims)
    # Compute median
    obs_med_t = np.median(obs_st, axis=0)
    # Compute 5th-percentile  
    obs_p05_t = np.percentile(obs_st, 5, axis=0)
    # Compute 95th-percentile
    obs_p95_t = np.percentile(obs_st, 95, axis=0)
    
    # Prepare output dictionary & store results
    tss_dict = {}
    tss_dict['avg'] = obs_avg_t
    tss_dict['std'] = obs_std_t
    tss_dict['l95'] = obs_l95_t
    tss_dict['u95'] = obs_u95_t
    tss_dict['med'] = obs_med_t
    tss_dict['p05'] = obs_p05_t
    tss_dict['p95'] = obs_p95_t

    return tss_dict


def extract_global_observables(results):
    
    # Unpack inputs
    pop_pht = results['pop']
    risk_pt = results['risk'] 

    # Obtain global-level time series
    global_s_t = np.sum(pop_pht[:,0], axis=0)
    global_i_t = np.sum(pop_pht[:,1], axis=0)
    global_r_t = np.sum(pop_pht[:,2], axis=0)
    N = global_s_t + global_i_t + global_r_t
    global_rsk_t = np.sum(risk_pt, axis=0)
    
    # Build distributions for certain global quantities
    inc_max = np.max(global_i_t, axis=0)
    ss_prev = global_r_t[-1]
    rsk_max = np.max(global_rsk_t, axis=0)

    # Prepare & store calculations in output dictionary
    obs_dict  = {'peak_incidence': inc_max, 'peak_risk': rsk_max,
                 'prevalence': ss_prev}

    return obs_dict


def extract_local_observables(results, pars):

    # Unpack inputs
    pop_pht = results['pop']
    cir_pt = results['cir']
    risk_pt = results['risk']

    hold = pars['hold']
    
    city_name = pars['city']
    if 'hold' in pars.keys():
        hold = pars['hold']
    else:
        hold = True
    
    patch_name_list = du.get_patch_name_list(city_name)
    V = len(pop_pht)
    
    # Prepare output dictionary
    obs_dict = {}
    
    for patch in range(0, V):

        # Obtain local-level time series
        i_t = pop_pht[patch,1]
        cir_t = cir_pt[patch]
        rsk_t = risk_pt[patch]
        
        # Compute risk status
        risk_status = rsk_t[-1]
        
        # Compute hitting time & end time
        nonzero_array = np.nonzero(i_t)
        if nonzero_array[0].size:
            hitting_time = np.min(np.nonzero(i_t))
            end_time = np.max(np.nonzero(i_t)) + 1
        else:
            hitting_time = np.nan
            end_time = 0
            
        # Compute CIR above thresholds times
        index_array = np.where(cir_t > 20)[0]
        if index_array.size:
            over20cir_time = index_array[0]
        else:
            over20cir_time = np.nan
        index_array = np.where(cir_t > 100)[0]
        if index_array.size:
            over100cir_time = index_array[0]
        else:
            over100cir_time = np.nan
        index_array = np.where(cir_t > 500)[0]
        if index_array.size:
            over500cir_time = index_array[0]
        else:
            over500cir_time = np.nan
        index_array = np.where(cir_t > 1000)[0]
        if index_array.size:
            over1000cir_time = index_array[0]
        else:
            over1000cir_time = np.nan
        
        # Compute ban & lift times
        nonzero_array2 = np.nonzero(rsk_t)
        if nonzero_array2[0].size:
            ban_time = np.min(np.nonzero(rsk_t))
            lift_time = np.max(np.nonzero(rsk_t)) + 1
        else:
            ban_time = np.nan
            lift_time = 0
        if hold == False:
            lift_time = end_time
        inc_max_time = np.argmax(i_t, axis=0)
        rsk_max_time = np.argmax(rsk_t, axis=0)

        # Prepare & store calculations in output dictionary
        patch_name = patch_name_list[patch]
        obs_dict[patch_name]  = {'hit': hitting_time,
                                 'o20': over20cir_time,
                                 'o100': over100cir_time,
                                 'o500': over500cir_time,
                                 'o1000': over1000cir_time,
                                 'ban': ban_time,
                                 'pit': inc_max_time,
                                 'prt': rsk_max_time,
                                 'end': end_time,
                                 'rsk': risk_status}

    return obs_dict


def extract_time_series_statistics(obs_st):

    # Compute average trajectory
    obs_avg_t = np.mean(obs_st, axis=0)
    # Compute standard deviation
    obs_std_t = np.std(obs_st, axis=0)
    # Compute 95% confidence interval
    z = 1.96
    nsims = len(obs_st)
    obs_l95_t = obs_avg_t - (z * obs_std_t / np.sqrt(nsims))
    obs_u95_t = obs_avg_t + (z * obs_std_t / np.sqrt(nsims))
    # Compute median
    obs_med_t = np.median(obs_st, axis=0)
    # Compute 5th-percentile  
    obs_p05_t = np.percentile(obs_st, 5, axis=0)
    # Compute 95th-percentile
    obs_p95_t = np.percentile(obs_st, 95, axis=0)
    
    # Prepare output dictionary & store results
    tss_dict = {}
    tss_dict['avg'] = obs_avg_t
    tss_dict['std'] = obs_std_t
    tss_dict['l95'] = obs_l95_t
    tss_dict['u95'] = obs_u95_t
    tss_dict['med'] = obs_med_t
    tss_dict['p05'] = obs_p05_t
    tss_dict['p95'] = obs_p95_t

    return tss_dict


def extract_distribution_statistics(dist):
    
    dist_ = dist.copy()
    dist = dist_[~np.isnan(dist)]
    
    if dist.size == False:
        dist = dist_.copy()

    # Compute average value of the distribution
    dist_avg = np.mean(dist)
    # Compute standard deviation
    dist_std = np.std(dist)
    # Compute 95% confidence interval
    z = 1.96
    nsims = len(dist)
    dist_l95 = dist_avg - (z * dist_std / np.sqrt(nsims))
    dist_u95 = dist_avg + (z * dist_std / np.sqrt(nsims))
    # Compute median
    dist_med = np.median(dist)
    # Compute 5th-percentile
    dist_p05 = np.percentile(dist, 5)
    # Compute 95th-percentiñe
    dist_p95 = np.percentile(dist, 95)
    
    # Prepare output dictionary & store results
    dist_dict = {}
    dist_dict['avg'] = dist_avg
    dist_dict['std'] = dist_std
    dist_dict['l95'] = dist_l95
    dist_dict['u95'] = dist_u95
    dist_dict['med'] = dist_med
    dist_dict['p05'] = dist_p05
    dist_dict['p95'] = dist_p95
    dist_dict['nsims'] = nsims

    return dist_dict


def outline_results(results, pars):
    """ Compute summary statistics for the distributions of peak incidence,

    """

    # Load parameters
    theta = pars['theta']
    kappa = pars['kappa']
    N = results['N']
    V = results['V']

    # Filter outbreaks
    pin_d = select_valid_outbreaks(results, 'pin_d', theta, kappa)
    pre_d = select_valid_outbreaks(results, 'pre_d', theta, kappa)
    rsk_d = select_valid_outbreaks(results, 'rsk_d', theta, kappa)

    # Get statistics dict
    pin_dict = extract_distribution_statistics(pin_d)
    pre_dict = extract_distribution_statistics(pre_d)
    rsk_dict = extract_distribution_statistics(rsk_d)

    # Get results
    pin_avg = (pin_dict['avg'] / N) * 100.0
    pin_l95 = (pin_dict['l95'] / N) * 100.0
    pin_u95 = (pin_dict['u95'] / N) * 100.0
    pre_avg = (pre_dict['avg'] / N) * 100.0
    pre_l95 = (pre_dict['l95'] / N) * 100.0
    pre_u95 = (pre_dict['u95'] / N) * 100.0
    rsk_avg = (rsk_dict['avg'] / V) * 100.0
    rsk_l95 = (rsk_dict['l95'] / V) * 100.0
    rsk_u95 = (rsk_dict['u95'] / V) * 100.0

    # Print results
    print("Peak incidence (%). Avg: {0} with 95-CI [{1}, {2}]".format(round(pin_avg, 2), round(pin_l95, 2), round(pin_u95, 2)))
    print("Prevalence (%). Avg: {0} with 95-CI [{1}, {2}]".format(round(pre_avg, 2), round(pre_l95, 2), round(pre_u95, 2)))
    print("Disticts at risk (%). Avg: {0} with 95-CI [{1}, {2}]".format(round(rsk_avg, 2), round(rsk_l95, 2), round(rsk_u95, 2)))


def select_valid_outbreaks(results, obs, theta, kappa):
    # Set separation threshold criterion (number of invaded patches)
    # the magic numbers are the result of a visual exploration of the outbreak distribution
    if theta == 20:
        if kappa >= 1e-1:    
            separation_threshold = 7 
        else:
            separation_threshold = 1
    elif theta == 100:
        if kappa >= 1e-2:
            separation_threshold = 7
        else:
            separation_threshold = 1
    elif theta == 500:
        if kappa >= 1e-2:
            separation_threshold = 7
        elif kappa >= 1e-3:
            separation_threshold = 3
        else:
            separation_threshold = 1
    elif theta == 1000:
        if kappa >= 1e-2:
            separation_threshold = 7
        elif kappa >= 1e-3:
            separation_threshold = 3
        else:
            separation_threshold = 1
    else:
        separation_threshold = 1000
        
        pre_d = results['pre_d']
        if obs == 'pin_d':
            filter_obs_d = results['pin_d'][pre_d >= separation_threshold]
        elif obs == 'pre_d':
            filter_obs_d = results['pre_d'][pre_d >= separation_threshold]

        return filter_obs_d

    # Filter outbreaks
    rsk_d = results['rsk_d']
    if obs == 'pin_d':
        filter_obs_d = results['pin_d'][rsk_d >= separation_threshold]
    elif obs == 'pre_d':
        filter_obs_d = results['pre_d'][rsk_d >= separation_threshold]
    elif obs == 'rsk_d':
        filter_obs_d = results['rsk_d'][rsk_d >= separation_threshold]

    return filter_obs_d


def plot_outbreak_distribution(results):
    # Function used to visually explore the outbreak distribution of a simulation and
    # set a criterion to separate valid outbreaks and failed outbreaks.
    # This is due to the fact that in stochastic simulations even if R0>1, the outbreak
    # can die out. Thus only the solutions corresponding with the deterministic solution
    # are collected.
    
    # Extract data
    par_tuple = list(results.keys())[0]
    theta = par_tuple[0]
    kappa = par_tuple[1]
    chi = par_tuple[2]
    V = results[par_tuple]['V']
    pre_d = results[par_tuple]['pre_d']
    rsk_d = results[par_tuple]['rsk_d']
    
    # Prepare bins to classify
    pre_min = 0
    pre_max = int(np.max(pre_d) + 0.5)
    pre_line = np.linspace(pre_min, pre_max, 20, dtype=np.int_)
    pre_bins = len(pre_line)
    rsk_line = np.arange(0, 22, 1, dtype=np.int_)
    rsk_bins = len(rsk_line) + 1
    
    # Classify
    freq_matrix = np.zeros((pre_bins, rsk_bins), dtype=np.int_)
    nsims = len(pre_d)
    for i in range(nsims):
        
        for j in range(pre_bins - 1):
            if pre_d[i] < pre_line[j+1]:
                pre_pos = j
                break;
        for k in range(rsk_bins):
            if rsk_d[i] == rsk_line[k]:
                rsk_pos = k
                break;
        freq_matrix[j,k] += 1
    
    import matplotlib.pyplot as plt
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)
    
    Z = np.zeros((pre_bins, rsk_bins), dtype=np.int_)
    for j in  range(pre_bins):
            h = pre_bins - j - 1
            for k in  range(rsk_bins):
                Z[h][k] = freq_matrix[j][k]
    
    im1 = ax.imshow(Z, cmap='plasma')
    
    colormap = plt.cm.get_cmap('plasma') # 'plasma' or 'viridis'
    colors = colormap(Z)
    sm = plt.cm.ScalarMappable(cmap=colormap)
    sm.set_clim(vmin=np.min(Z), vmax=np.max(Z))
    fig.colorbar(sm)
    
    # Plotting settings
    res_pre_line = pre_line[::-1]
    r_pre_line = np.round(res_pre_line, decimals=5)
    r_rsk_line = np.round(rsk_line, decimals=2)
    t_gp = [str(r_pre_line[i]) for i in range(0, len(pre_line), 1)]
    t_gr = [str(r_rsk_line[i]) for i in range(0, len(rsk_line), 1)]
    ax.set_yticks(range(0, len(pre_line), 1), minor=False)
    ax.set_xticks(range(0, len(rsk_line), 1), minor=False)
    ax.set_yticklabels(t_gp, fontdict=None, minor=False)
    ax.set_xticklabels(t_gr, fontdict=None, minor=False, fontsize=8)
    ax.set_xlabel(r'patches at risk')
    ax.set_ylabel(r'prevalence')
    ax.set_title(r'$\Theta={0}$, $\kappa={1}$, $\chi={2}$'.format(theta, kappa, chi))
    fig.suptitle('Outbreak distribution.')