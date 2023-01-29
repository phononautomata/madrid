#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:41:03 2021

@author: ademiguel

This file hosts the building blocks of PERIMETRAL project's model.
The model used is a metapopulation SIR epidemic model with real mobility
data that implements perimeter lockdowns.  

The main purpose of this project is to explore the efficacy of perimetral
lockdowns (patch-level confinements) in the spreading of a disease in a urban
environment. The focus of our manuscript is the city of Madrid, Spain, but
this can be applied elsewhere or even posed as an abstract fully theoretical
problem.

The spatial structure is represented as a metapopulation network. Every
subpopulation or patch is a subdivision of a city. The network of patches is
fully connected, meaning that every individual may travel from one patch to 
any other directly. The flows of individuals along patches are informed
with real mobility data.

The patches are populated with real figures of the corresponding urban
districts. There is however no internal structure and a well-mixed
approximation takes place inside each of them. 

A risk indicence threshold may be considered in order to set travel bans
among patches or patch-level lockdowns. This threshold or index is local and
once surpassed, the patch may be partially or totally closed to inflows and
outflows of individuals. Additionally, once this happens, further measures can 
be taken in the form of disease awareness and social distancing, which 
translates into a certain reduction of the reproduction number within 
the patch.

Disclaimer: this code allowed to obtain the result for the manuscript and 
consequently has been checked. It is now being offered publicly but there 
is still a lot of work to do regarding code organization, documentation, 
refactoring, error handling, and so on.

"""

#from numba import njit
import numpy as np

import data_utils as du
import analysis as an

#@njit
def multinomial(n, pvals):
    
    # Numpy's algorithm for multinomial()
    plen = len(pvals)
    fl = np.zeros(plen, dtype=np.int_)
    sz = plen

    for i in range(0, sz, plen):
        # Loop body: take a set of n experiments and fill up
        # fl[i:i + plen] with the distribution of results.

        # Current sum of outcome probabilities
        p_sum = 1.0
        # Current remaining number of experiments
        n_experiments = n
        # For each possible outcome `j`, compute the number of results
        # with this outcome.  This is done by considering the
        # conditional probability P(X=j | X>=j) and running a binomial
        # distribution over the remaining number of experiments.
        for j in range(0, plen - 1):
            p_j = pvals[j]
            p = min(p_j / p_sum, 1.0)
            n_j = fl[i + j] = np.random.binomial(n_experiments, p)
            n_experiments -= n_j
            if n_experiments <= 0:
                # Note the output was initialized to zero
                break
            p_sum -= p_j
        if n_experiments > 0:
            # The remaining experiments end up in the last bucket
            fl[i + plen - 1] = n_experiments
    
    return fl


def seed_epidemic(pop_patch, epicenter, seeds, mod_id):
    """
    Initialize the epidemic model by setting the number of seeds or index
    cases (zero patients) in a certain patch. No multi-seeding allowing here.
    
    Population is stored in a V*H matrix, where V is number of patches in the
    system and H is number of health statuses. For the SIR model, 0 belongs to 
    susceptible health status, 1 to infected and 2 to removed. For the SEIR 
    model, 1 belongs to exposed, 2 to infectious and then 3 to removed.
    
    Parameters
    ----------
    pop_patch : int array
        Every patch's population.
    epicenter : int
        Patch's integer index where the spreading starts.
    seeds : int
        Number of index cases.
    mod_id : str
        Epidemic model identifier ('SIR' or 'SEIR').
    
    Returns
    -------
    pop: 2d int array
        Number of individuals in a certain patch with a certain health status.

    """
    
    if mod_id == 'SIR':
        S = 1
        H = 3
    else:
        print('MODEL IDENTIFIER ERROR. DEFAULT: SIR model')

    V = len(pop_patch)
    pop = np.zeros((V, H), dtype=np.int_)
    pop[:].T[0] = pop_patch
    pop[epicenter][0] -= seeds
    pop[epicenter][S] += seeds
    
    return pop


#@njit
def set_travel_bans(origin, travelers, risk_array):
    """
    Modify the flows of traveling individuals among an origin patch and all
    possible destinations regarding epidemic risk. 

    If origin patch is at risk, individuals to travel to other patches should 
    stay within their origin (outflow banning). If either any destination patch 
    is at risk, individuals traveling there should stay within origin 
    (inflow banning). An adherence parameter is regarded to potentially explore 
    compliance with these restrictions (or imperfections).
    
    Parameters
    ----------
    origin : int
        Index of patch where the trip starts.
    travelers : array
        Number of travelers from origin patch to every patch (origin included).
    risk_array : int array
        Every patch risk condition. 1 is above risk threshold, 0 is below.
    adherence : float
        Fraction of population complying with travel bans.
    
    Returns
    -------
    None.

    """

    V = len(travelers)
    if risk_array[origin] == 1: # if origin at risk everyone stays within
        temp = np.sum(travelers)
        travelers[:] = 0
        travelers[origin] = temp
    else: # no? then take back all those going to risk destinations
        for dest in range(0, V):
            if dest != origin and risk_array[dest] == 1:
                travelers[origin] += travelers[dest]
                travelers[dest] = 0
 

def set_inner_restrictions(beta, risk_array, chi=1.0):
    """
    Modify a patch's transmissibility rate if at risk.

    Parameters
    ----------
    beta : float
        Original transmissibility rate.
    risk_array : int array
        Every patch risk condition. 1 is above risk threshold, 0 is below.
    chi : float
        Fraction of the transmissibility if patch is at risk.
    
    Returns
    -------
    beta_array : float array
        Every patch's transmissibility rate.

    """

    beta_array = np.full(len(risk_array), beta)
    beta_array[risk_array == 1] = beta_array[risk_array == 1] * chi

    return beta_array

    
def compute_CIR(cir, t, pop_pht, newcases_pt, t_span):

    if t - t_span < 0:
        t_span = t
        
    #cir[:] = np.sum(newcases_pt[:,t-t_span:t+1], axis=1) * 1e+5 / pop_pht[:,0,t-t_span] #old version, minor differences
    cir[:] = np.sum(newcases_pt[:,t-t_span:t+1], axis=1) * 1e+5 / np.sum(pop_pht[:,:,0], axis=1)

    return cir


#@njit
def reaction_core(pop, beta_array, T_I, newcases):
    """
    Perform the stochastic computation of the epidemic reactions for every 
    patch of the metapopulation system. 
    
    Transitions from susceptible to infected state (S->I) in case of SIR model, 
    or from susceptible to exposed state (S->E) in case of SEIR model are 
    evaluated under the homogeneous well-mixing approximation and a 
    frequency-dependent force of infection. All decay transitions (I->R, E->I) 
    are Markovian. The number of new cases (either exposed, infected or 
    removed) is drawn from binomial distributions to speed up computations.

    Populations in every patch and health status are updated after the
    patch's epidemic reactions have taken place.

    Parameters
    ----------
    pop : 2d int array
        Number of individuals in a certain patch with a certain health status.
    R0_array : float array
        Every patch's basic reproduction number.
    T_I : float
        Infectious period in days.
    newcases : int array
        Number of new cases produced in each patch at the time-step.

    Returns
    -------
    None.

    """
    
    # Perform infection reactions in every patch & update
    V = len(pop)
    for patch in range(0, V):
        
        # Preparations
        new_cases = 0 # I in SIR, E in SEIR
        new_removed = 0
        N_patch = np.sum(pop[patch])
        N_S = pop[patch][0]
        N_I = pop[patch][1]
        
        # Extract removed individuals & update removed
        if N_I != 0:
            rem_prob = (1.0 / T_I)
            new_removed = np.random.binomial(N_I, rem_prob)
            pop[patch][2] += new_removed

        # Extract new infected cases & update susceptible
        if N_patch == 0: # case of depopulated patch
            noninf_prob = 0.0
        else:
            noninf_prob = 1.0 - (beta_array[patch] / N_patch) # FoI enters here
        contagion_prob = 1.0 - np.power(noninf_prob, N_I)
        if (N_S != 0 and contagion_prob != 0):
            new_cases = np.random.binomial(N_S, contagion_prob)
            pop[patch][0] -= new_cases
            newcases[patch] += new_cases

        # Update infected individuals for SIR
        pop[patch][1] += (new_cases - new_removed)


#@njit
def diffusion_core(pop, od_matrix, risk_array):
    """
    Perform the stochastic computation of the diffusion 
    of individuals for every patch of the metapopulation system. 

    The diffusion process uses a diffusion rate (origin-destination) matrix 
    with real mobility and a mobility parameter kappa is coupled to 
    off-diagonal elements to calibrate the outflows with respect to a baseline
    scenario. The number of new travelers in every health status to every patch 
    is drawn from respective multinomial distributions.
    
    Populations in every patch and health status are updated during and after 
    the whole diffusion process.

    Parameters
    ----------
    pop : 2d int array
        Number of individuals in a certain patch with a certain health status.
    od_matrix : 2d float array
        Probability of reaching patch j from patch i (data-driven).
    risk_array : int array
        Every patch risk condition. 1 is above risk threshold, 0 is below.

    Returns
    -------
    None.

    """
    
    V = len(pop)
    H = len(pop[0])
    travelers_matrix = np.zeros((V, V, H), dtype=np.int_)
    
    # Build travelers matrix from every patch to every other (multinomial)
    # Travel bans are revised if local risk condition holds
    for patch in range(0, V):
        
        flow_rates = od_matrix[patch]
        N_S = pop[patch][0]
        N_I = pop[patch][1]
        N_R = pop[patch][2]

        if N_S != 0: 
            s_travelers = multinomial(N_S, flow_rates)
            #s_travelers = np.random.multinomial(N_S, flow_rates)
            if np.sum(risk_array) != 0:
                set_travel_bans(patch, s_travelers, risk_array)
            travelers_matrix[patch,:,0] += s_travelers

        if N_I != 0:
            i_travelers = multinomial(N_I, flow_rates)
            #i_travelers = np.random.multinomial(N_I, flow_rates)
            if np.sum(risk_array) != 0:
                set_travel_bans(patch, i_travelers, risk_array)
            travelers_matrix[patch,:,1] += i_travelers

        if N_R != 0:
            r_travelers = multinomial(N_R, flow_rates)
            #r_travelers = np.random.multinomial(N_R, flow_rates)
            if np.sum(risk_array) != 0:
                set_travel_bans(patch, r_travelers, risk_array)
            travelers_matrix[patch,:,2] += r_travelers
    
    # Rearrange flows in order to conserve local populations
    symmetrize_flows(pop, travelers_matrix)


#@njit
def symmetrize_flows(pop, travelers_matrix):
    """
    Symmetrize direct and reverse flows among patches in order to conserve
    original patch population sizes.
    
    For a pair of origin-destination patches there is always a flow in one
    direction and another in the reverse one. To avoid further complications
    the minimum flow of total travelers among those patches is chosen and 
    individuals are transported accordingly (direct flows). Then, the remaining
    flows of individuals (reverse flows) are obtained from the corresponding
    origin patch. Now, the total number of travelers is fixed by the direct 
    flow, and thus individuals to travel are sampled not from the diffusion
    rate matrix but from the proportions of individuals in every health status
    in the corresponding patch. Checks exist to avoid transporting a higher 
    number of individuals of a certain health status higher than those existing.

    Parameters
    ----------
    pop : 2d int array
        Number of individuals in a certain patch with a certain health status.
    travelers_matrix : 3d int array
        Number of individuals in each health status traveling between a pair
        of patches.

    Returns
    -------
    None.

    """

    # Obtain minimum flows & make a first update of populations
    V = len(pop)
    minimum_flow = np.zeros((V, V), dtype=np.int_)

    for ori in range(0, V):
        for des in range(0, V):
            if ori >= des:
                
                # This is a matter of convention (direct-reverse)
                direct_flow = np.sum(travelers_matrix[ori][des])
                reverse_flow = np.sum(travelers_matrix[des][ori])
                
                # Minimum flows chosen & exchange done with population update
                if direct_flow <= reverse_flow:
                    minimum_flow[ori][des] = direct_flow
                    pop[des] += travelers_matrix[ori][des]
                    pop[ori] -= travelers_matrix[ori][des]
                else:
                    minimum_flow[des][ori] = reverse_flow
                    pop[des] -= travelers_matrix[des][ori]
                    pop[ori] += travelers_matrix[des][ori]

    # Complete remaining flows, sample travelers & update populations
    temp_pop = pop.copy()
    for ori in range(0, V):
        for des in range(0, V):
            if minimum_flow[ori][des] == 0:
                
                # Build reverse flow
                travelers = minimum_flow[des][ori]
                pop_props = temp_pop[ori] / np.sum(temp_pop[ori])
                
                # Check compartmental population conservation laws
                conservation_condition = False
                while conservation_condition == False:
                    travelers_array = multinomial(travelers, pop_props)
                    #travelers_array = np.random.multinomial(travelers, pop_props)
                    s_check = not (travelers_array[0] > temp_pop[ori][0])
                    i_check = not (travelers_array[1] > temp_pop[ori][1])
                    r_check = not (travelers_array[2] > temp_pop[ori][2])
                    if (s_check and i_check and r_check) == True:
                        conservation_condition = True
                
                # Exhaust 'used' travelers
                travelers_matrix[ori][des] = travelers_array
                temp_pop[ori] -= travelers_array
                
                # Update populations                
                pop[ori] -= travelers_matrix[ori][des]
                pop[des] += travelers_matrix[ori][des]


def dynamical_loop(pop0, od_matrix, R0, T_I, T_MAX, theta=1.0, chi=1.0, 
                   hold=True, t_span=13):
    """
    Perform the dynamical loop of the model. That is, execute one stochastic 
    run of the metapopulation data-driven mobility epidemic dynamics. 
    
    The dynamical loop starts with the initialized system, performs
    the reaction and diffusion steps, together with the risk analysis and 
    response if proceeds, and moves to the next time-step. The dynamical
    loop is executed until the absorbing state for the model is reached
    (either no infected individuals for SIR, and no exposed and infected
    for SEIR model), or a predetermined amount of time has elapsed.
    
    At the end of the loop, a time series for every patch and health status
    populations is recorded and returned, together with the time series of
    risk-state of every patch during the spreading. Additionally, more global
    and local support observables are recorded.

    Parameters
    ----------
    pop : 2d int array
        Number of individuals in a certain patch with a certain health status.
    od_matrix : 2d float array
        Probability of reaching patch j from patch i (data-driven).
    R0 : float
        Basic reproduction number.
    T_I : float
        Infectious period in days.
    T_MAX : int
        Maximum number of days to run the model.
    threshold : float
        Risk indicence threshold.
    chi : float
        Fraction of the transmissibility if patch is at risk.

    Returns
    -------
    output : dict
        Contains several observable t-series for further analysis.

    """

    # Compute transmission rate from given R0
    beta = R0 / T_I
    
    # Prepare & initialize arrays
    V = len(pop0)
    H = len(pop0[0])
    pop_pht = np.zeros((V, H, T_MAX), dtype=np.int_)
    pop_pht[:,:,0] = pop0
    pop = pop0.copy()
    cir_pt = np.zeros((V, T_MAX), dtype=np.float)
    cir = cir_pt[:,0].copy() # not correctly initialized to be honest
    newcases_pt = np.zeros((V, T_MAX), dtype=np.int_)
    newcases = newcases_pt[:,0].copy()
    newcases_pt[:,0] = pop0[:,1]
    risk_array = np.zeros(V, dtype=np.int_)
    risk_pt = np.zeros((V, T_MAX), dtype=np.int_)
    risk_pt[:,0] = risk_array.copy()
    R0_array = np.full(V, R0)
    Rt_pt = np.zeros((V, T_MAX), dtype=np.float)
    Rt_pt[:,0] = R0_array * pop.T[0]
    Rt_gt = np.zeros(T_MAX, dtype=np.float)
    Rt_gt[0] = R0 * np.sum(pop.T[0]) / np.sum(pop)
    
    # Initialize time and set default conditions to enter the loop
    t = 0
    total_infected = 1 # default to enter the while-loop

    # Loop dynamics until time out or absorbing state
    while (t < T_MAX-1 and (total_infected != 0)):

        # Local risk response: update patches at risk
        risk_condition = cir >= theta
        risk_array[risk_condition] = 1
        if hold == False:
            safe_condition = cir < theta
            risk_array[safe_condition] = 0
        if np.sum(risk_array) != 0:
            beta_array = set_inner_restrictions(beta, risk_array, chi)
            R0_array = beta_array * T_I
            Rt_array = R0_array * pop.T[0]
        else:
            beta_array = np.full(V, beta)
            R0_array = beta_array * T_I
            Rt_array = R0_array * pop.T[0]

        # Reaction-diffusion dynamics (populations updated inside)
        reaction_core(pop, beta_array, T_I, newcases)
        diffusion_core(pop, od_matrix, risk_array)
        
        # Compute Cumulative-Incidence-Rate in every patch
        compute_CIR(cir, t, pop_pht, newcases_pt, t_span)

        # Obtain macrostates
        total_infected = np.sum(pop[:].T[1])
        total_removed = np.sum(pop[:].T[-1])
        total_risk = np.sum(risk_array)

        # Next time-step (in days)
        t += 1

        # Store results in outpuy arrays
        pop_pht[:,:,t] = pop.copy()
        cir_pt[:,t] = cir.copy()
        newcases_pt[:,t] = newcases.copy()
        risk_pt[:,t] = risk_array.copy()
        Rt_pt[:,t] = Rt_array.copy()
        Rt_gt[t] = R0 * np.sum(pop.T[0]) / np.sum(pop)
        # Reset temporary array
        newcases = np.zeros(V, dtype=np.int_)

        #print('Incidence={0}, Prevalence={1}, Risk={2} at time t={3}'.format(total_infected, total_removed, total_risk, t))
        #print('Total risk={0}'.format(np.sum(risk_pt[:,t])))
        #print('14d-CIR={0}'.format(cir))

    print('Incidence={0}, prevalence={1}, risk={2} at t={3}'.format(total_infected, total_removed, total_risk, t))

    # Assess outbreak size
    total_pop = np.sum(pop)
    if total_removed < 0.01 * total_pop:
        large_outbreak = False
    else:
        large_outbreak = True

    # Complete output arrays
    while t < T_MAX:
        pop_pht[:,:,t] = pop.copy()
        cir_pt[:,t] = cir.copy()
        risk_pt[:,t] = risk_array.copy()
        Rt_pt[:,t] = Rt_array.copy()
        Rt_gt[t] = R0 * np.sum(pop.T[0]) / np.sum(pop)
        t += 1
    
    # Store observables into output dictionary
    output = {}
    output['pop'] = pop_pht
    output['cir'] = cir_pt
    output['risk'] = risk_pt
    output['Rt'] = Rt_pt
    output['Rt_g'] = Rt_gt
    output['size'] = large_outbreak

    return output



def launch_model(pars):
    """
    Iniatilize and run a series of realizations for the stochastic 
    metapopulation data-driven mobility epidemic model. 

    The model needs to be informed with the place where it is going to be run 
    and a related subdivision where the epidemic will start. Then, real 
    population data for each subdivision is imported, together with mobility 
    data in order to build an origin-destination matrix for the diffusion 
    process.
    
    The model is ready for the dynamics after some index cases are introduced
    in a patch of the metapopulation system. After an epidemic run is done,
    time series results for the simulation are stored. After all demanded 
    stochastic realizations finish, an array with time series of populations
    of every health status in every patch and for every simulation is returned
    to perform some statistics and analysis.

    This version includes an inner filter for mitigating failed outbreaks 
    collection. Depending on the input parameters given it may not get valid
    outbreaks at all. The results for the manuscript were obtained somewhat
    differently, by allowing all kinds of outbreak sizes and extensions and 
    then filtering in a post-processing phase.

    Parameters
    ----------
    city : str
        Name of the city or whatever the full metapopulation system is.
    epicenter : int
        Integer index for the patch where the epidemic starts.
    pop_patch : int array
        Every patch's population.
    seeds : int
        Number of index cases.
    mod_id : str
        Epidemic model identifier ('SIR' or 'SEIR').
    mob_id : str
        Mobility scenario identifier.
    travel_matrix : 2d float array 
        Average number of travels in a specified period between a pair of patches.
    kappa : float
        Mobility parameter to scale with respect to reference mobility.
    nsims : int
        Number of simulations for the stochastic dynamics.
    T_MAX : int
        Maximum number of days to run the model.
    R0 : float
        Basic reproduction number.
    T_I : float
        Infectious period in days.
    theta : float
        Risk incidence threshold.
    chi : float
        Fraction of the transmissiblity if patch is at risk.
    epsilon : float
        Fraction of population complying with travel bans.
    hold : bool
        Hold restrictions until the full end of the spreading
    t_span : int
        Period of time for the Cumulative Incidence Rate observable

    Returns
    -------
    output : dict
        Contains the following keys : values pairs:
            'pops' : 2d int array
            Every patch's population by health status time series.
            'risk' : int array
            Every patch's risk status time series.
    """
    
    # Unpack parameters
    city = pars['city']
    patch_id = pars['patch_id']
    mod_id = pars['mod_id']
    mob_id = pars['mob_id']
    kappa = pars['kappa']
    seeds = pars['seeds']
    R0 = pars['R0']
    T_I = pars['T_I']
    nsims = pars['nsims']
    T_MAX = pars['T_MAX']
    theta = pars['theta']
    chi = pars['chi']
    hold = pars['hold']
    t_span = pars['tspan']
    local = pars['local']

    # Get patches populations
    pop_patch = du.import_population(city, '2020')
 
    # Set the epicenter
    epicenter = du.extract_patch_integer_index(city, patch_id)
 
    # Import diffusion matrix
    travel_matrix = du.build_averaged_travel_matrix(city, mob_id)
 
    # Occupy patches and introduce zero patients
    pop0 = seed_epidemic(pop_patch, epicenter, seeds, mod_id)

    # Build diffusion rate matrix
    od_matrix = du.build_data_driven_diffusion_matrix(travel_matrix, kappa)

    # Prepare observables
    V = len(pop_patch)
    H = len(pop0[0])
    pop_spht = np.zeros((nsims, V, H, T_MAX), dtype=np.int_)
    cir_spt = np.zeros((nsims, V, T_MAX), dtype=np.float_)
    risk_spt = np.zeros((nsims, V, T_MAX), dtype=np.int_)
    Rt_spt = np.zeros((nsims, V, T_MAX), dtype=np.float)
    Rt_st = np.zeros((nsims, T_MAX), dtype=np.float_)
    pin_d = np.zeros(nsims, dtype=np.int_) # peak incidence distribution
    pre_d = np.zeros(nsims, dtype=np.int_) # steady-state prevalence distribution
    rsk_d = np.zeros(nsims, dtype=np.int_) # steady-state patches at risk distribution
    if local == True:
        loc_dict = {}

    # Loop over different dynamical realizations
    for sim in range(0, nsims):

        print('Realization {0}. R0={1}, theta={2}, kappa={3}, chi={4}'.format(sim, R0, theta, kappa, chi))
        
        results = dynamical_loop(pop0, od_matrix, R0, T_I, T_MAX, theta, chi, 
                hold, t_span)

        # Extract relevant global observables
        obs_dict = an.extract_global_observables(results)
        # Extract relevant local observables
        if local == True:
            loc_dict[sim] = an.extract_local_observables(results, pars)
        pop_spht[sim] = results['pop']
        cir_spt[sim] = results['cir']
        pre_d[sim] = obs_dict['prevalence']
        pin_d[sim] = obs_dict['peak_incidence']
        rsk_d[sim] = obs_dict['peak_risk']
        Rt_st[sim] = results['Rt_g']
        risk_spt[sim] = results['risk']

    # Prepare output
    output = {}
    output['N'] = np.sum(pop_patch)
    output['V'] = len(pop_patch)
    output['R0'] = R0
    output['pops'] = pop_spht
    output['risk'] = risk_spt
    output['Rt'] = Rt_spt
    output['cir'] = cir_spt
    output['pin_d'] = pin_d
    output['pre_d'] = pre_d
    output['rsk_d'] = rsk_d
    output['Rt_g'] = Rt_st
    if local == True:
        output['loc_dict'] = loc_dict

    return output


def launch_filtered_model(pars):
    """
    Iniatilize and run a series of realizations for the stochastic 
    metapopulation data-driven mobility epidemic model. 

    The model needs to be informed with the place where it is going to be run 
    and a related subdivision where the epidemic will start. Then, real 
    population data for each subdivision is imported, together with mobility 
    data in order to build an origin-destination matrix for the diffusion 
    process.
    
    The model is ready for the dynamics after some index cases are introduced
    in a patch of the metapopulation system. After an epidemic run is done,
    time series results for the simulation are stored. After all demanded 
    stochastic realizations finish, an array with time series of populations
    of every health status in every patch and for every simulation is returned
    to perform some statistics and analysis.

    This version includes an inner filter for mitigating failed outbreaks 
    collection. Depending on the input parameters given it may not get valid
    outbreaks at all. The results for the manuscript were obtained somewhat
    differently, by allowing all kinds of outbreak sizes and extensions and 
    then filtering in a post-processing phase.

    Parameters
    ----------
    city : str
        Name of the city or whatever the full metapopulation system is.
    epicenter : int
        Integer index for the patch where the epidemic starts.
    pop_patch : int array
        Every patch's population.
    seeds : int
        Number of index cases.
    mod_id : str
        Epidemic model identifier ('SIR' or 'SEIR').
    mob_id : str
        Mobility scenario identifier.
    travel_matrix : 2d float array 
        Average number of travels in a specified period between a pair of patches.
    kappa : float
        Mobility parameter to scale with respect to reference mobility.
    nsims : int
        Number of simulations for the stochastic dynamics.
    T_MAX : int
        Maximum number of days to run the model.
    R0 : float
        Basic reproduction number.
    T_I : float
        Infectious period in days.
    theta : float
        Risk indicence threshold.
    chi : float
        Fraction of the transmissiblity if patch is at risk.
    epsilon : float
        Fraction of population complying with travel bans.
    hold : bool
        Hold restrictions until the full end of the spreading
    t_span : int
        Period of time for the Cumulative Incidence Rate observable

    Returns
    -------
    output : dict
        Contains the following keys : values pairs:
            'pops' : 2d int array
            Every patch's population by health status time series.
            'risk' : int array
            Every patch's risk status time series.
    """
    
    # Unpack parameters
    city = pars['city']
    patch_id = pars['patch_id']
    mod_id = pars['mod_id']
    mob_id = pars['mob_id']
    kappa = pars['kappa']
    seeds = pars['seeds']
    R0 = pars['R0']
    T_I = pars['T_I']
    nsims = pars['nsims']
    T_MAX = pars['T_MAX']
    theta = pars['theta']
    chi = pars['chi']
    hold = pars['hold']
    t_span = pars['tspan']
    local = pars['local']

    # Get patches populations
    pop_patch = du.import_population(city, '2020')
 
    # Set the epicenter
    epicenter = du.extract_patch_integer_index(city, patch_id)
 
    # Import diffusion matrix
    travel_matrix = du.build_averaged_travel_matrix(city, mob_id)
 
    # Occupy patches and introduce zero patients
    pop0 = seed_epidemic(pop_patch, epicenter, seeds, mod_id)

    # Build diffusion rate matrix
    od_matrix = du.build_data_driven_diffusion_matrix(travel_matrix, kappa)

    # Prepare observables
    V = len(pop_patch)
    H = len(pop0[0])
    pop_spht = np.zeros((nsims, V, H, T_MAX), dtype=np.int_)
    cir_spt = np.zeros((nsims, V, T_MAX), dtype=np.float_)
    risk_spt = np.zeros((nsims, V, T_MAX), dtype=np.int_)
    Rt_spt = np.zeros((nsims, V, T_MAX), dtype=np.float)
    Rt_st = np.zeros((nsims, T_MAX), dtype=np.float_)
    pin_d = np.zeros(nsims, dtype=np.int_) # peak incidence distribution
    pre_d = np.zeros(nsims, dtype=np.int_) # steady-state prevalence distribution
    rsk_d = np.zeros(nsims, dtype=np.int_) # steady-state patches at risk distribution
    if local == True:
        loc_dict = {}

    # Loop over different dynamical realizations
    for sim in range(0, nsims):

        print('Realization {0}. R0={1}, theta={2}, kappa={3}, chi={4}'.format(sim, R0, theta, kappa, chi))
        
        # Outbreak condition
        large_outbreak = False
        escape = 0

        while large_outbreak == False:
            results = dynamical_loop(pop0, od_matrix, R0, T_I, T_MAX, 
                                     theta, chi, hold, t_span)

            large_outbreak = results['size']
            escape += 1
            if escape >= 25:
                print('A small outbreak was accepted')
                large_outbreak = True
                escape = 0

        # Extract relevant global observables
        obs_dict = an.extract_global_observables(results)
        # Extract relevant local observables
        if local == True:
            loc_dict[sim] = an.extract_local_observables(results, pars)
        pop_spht[sim] = results['pop']
        cir_spt[sim] = results['cir']
        pre_d[sim] = obs_dict['prevalence']
        pin_d[sim] = obs_dict['peak_incidence']
        rsk_d[sim] = obs_dict['peak_risk']
        Rt_st[sim] = results['Rt_g']
        risk_spt[sim] = results['risk']

    # Prepare output
    output = {}
    output['N'] = np.sum(pop_patch)
    output['V'] = len(pop_patch)
    output['R0'] = R0
    output['pops'] = pop_spht
    output['risk'] = risk_spt
    output['Rt'] = Rt_spt
    output['cir'] = cir_spt
    output['pin_d'] = pin_d
    output['pre_d'] = pre_d
    output['rsk_d'] = rsk_d
    output['Rt_g'] = Rt_st
    if local == True:
        output['loc_dict'] = loc_dict

    return output