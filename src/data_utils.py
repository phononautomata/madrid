#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:54:02 2021

@author: ademiguel

This file hosts utilities for processing model's input data.
The model used is a metapopulation SIR epidemic model with real mobility
data that implements perimeter lockdowns.  

Since the model is informed with real data, some functions are needed to
organize and manage all the data related aspects.

Disclaimer: this code allowed to obtain the result for the manuscript and 
consequently has been checked. It is now being offered publicly but there 
is still a lot of work to do regarding code organization, documentation, 
refactoring, error handling, and so on.

"""

import os
import datetime

import numpy as np
import pandas as pd
import pickle as pk

path = os.path.dirname(os.getcwd())


def get_patch_code_integer_dictionary(city):
    """
    A dictionary for a series of cities where keys are names of its
    administrative or political subdivisions and related values are an
    integer index.

    Parameters
    ----------
    city : str
        Name of the city or whatever the full metapopulation system is.

    Returns
    -------
    patch_dict : dict
        City's subdivisions, keys are names, values are related integer codes.

    """
    
    if city == 'ZARAGOZA_juntas':
    
        patch_dict = {'CASCO_HISTORICO': 0, 'CENTRO': 1, 'DELICIAS': 2, 
                      'UNIVERSIDAD': 3, 'CASABLANCA': 4, 'DISTRITO_SUR': 5,
                      'SAN_JOSE': 6, 'LAS_FUENTES': 7, 'LA_ALMOZARA': 8,
                      'MIRALBUENO': 9, 'OLIVER_VALDEFIERRO': 10, 
                      'TORRERO_LA_PAZ': 11, 'ACTUR_REY_FERNANDO': 12,
                      'EL_RABAL': 13, 'SANTA_ISABEL': 14, 'LA_CARTUJA': 15,
                      'TORRECILLA_DE_VALMADRID': 16, 'JUSLIBOL_ZORONGO': 17,
                      'SAN_JUAN_DE_MOZARRIFAR': 18, 'MONTANANA': 19, 
                      'SAN_GREGORIO': 20, 'PENAFLOR': 21, 'MOVERA': 22, 
                      'GARRAPINILLOS': 23, 'VENTA_DEL_OLIVAR': 24, 
                      'MONZALBARBA': 25, 'VILLARRAPA': 26, 'ALFOCEA': 27,
                      'CASETAS': 28}
        
    elif city == 'ZARAGOZA':
        
        patch_dict = {'D1': 0, 'D2': 1, 'D3': 2, 'D4': 3, 'D5': 4, 'D6': 5, 
                      'D7': 6, 'D8': 7, 'D9': 8, 'D10': 9,'D11': 10, 'D12': 11}
        
    elif city == 'MADRID':
        
        patch_dict = {'CENTRO': 0, 'ARGANZUELA': 1, 'RETIRO': 2, 
                      'SALAMCANCA': 3, 'CHAMARTIN': 4, 'TETUAN': 5, 
                      'CHAMBERI': 6, 'FUENCARRAL_EL_PARDO': 7, 
                      'MONCLOA_ARAVACA': 8, 'LATINA': 9, 'CARABANCHEL': 10,
                      'USERA': 11, 'PUENTE_DE_VALLECAS': 12, 'MORATALAZ': 13,
                      'CIUDAD_LINEAL': 14, 'HORTALEZA': 15, 'VILLAVERDE': 16,
                      'VILLA_DE_VALLECAS': 17, 'VICALVARO': 18, 
                      'SAN_BLAS_CANILLEJAS': 19, 'BARAJAS': 20}
    
    return patch_dict


def extract_patch_integer_index(city, patch_id):
    """ 
    Extract the associated patch index as an integer number, given its string
    identifier.

    Parameters
    ----------
    city : str
        Name of the city or whatever the full metapopulation system is.
    patch_id : str
        Patch label identifier

    Returns
    -------
        : int
        Patch's integer index.

    """
    
    patch_dict = get_patch_code_integer_dictionary(city)

    return patch_dict[patch_id]


def get_patch_name_list(city):
    """
    A list containing the names of the patches for a given city.

    Parameters
    ----------
    city : str
        Name of the city or whatever the full metapopulation system is.

    Returns
    -------
    patch_list : str list
        List with name of patches.

    """
    
    if city == 'ZARAGOZA_juntas':
        
        patch_list = ['CASCO_HISTORICO', 'CENTRO', 'DELICIAS', 'UNIVERSIDAD', 
                      'CASABLANCA', 'DISTRITO_SUR', 'SAN_JOSE', 'LAS_FUENTES', 
                      'LA_ALMOZARA', 'MIRALBUENO', 'OLIVER_VALDEFIERRO', 
                      'TORRERO_LA_PAZ', 'ACTUR_REY_FERNANDO', 'EL_RABAL', 
                      'SANTA_ISABEL', 'LA_CARTUJA', 'TORRECILLA_DE_VALMADRID', 
                      'JUSLIBOL_ZORONGO', 'SAN_JUAN_DE_MOZARRIFAR', 
                      'MONTANANA', 'SAN_GREGORIO', 'PENAFLOR', 'MOVERA', 
                      'GARRAPINILLOS', 'VENTA_DEL_OLIVAR', 'MONZALBARBA', 
                      'VILLARRAPA', 'ALFOCEA', 'CASETAS']
    
    elif city == 'ZARAGOZA':
        
        patch_list = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 
                      'D9', 'D10', 'D11', 'D12']
        
    elif city == 'MADRID':
        
        patch_list = ['CENTRO', 'ARGANZUELA', 'RETIRO', 'SALAMANCA', 
                      'CHAMARTIN', 'TETUAN', 'CHAMBERI', 'FUENCARRAL_EL_PARDO', 
                      'MONCLOA_ARAVACA', 'LATINA', 'CARABANCHEL', 'USERA', 
                      'PUENTE_DE_VALLECAS', 'MORATALAZ', 'CIUDAD_LINEAL', 
                      'HORTALEZA', 'VILLAVERDE', 'VILLA_DE_VALLECAS', 
                      'VICALVARO', 'SAN_BLAS_CANILLEJAS', 'BARAJAS']
    
    else:
        
        patch_list = []

    return patch_list


def import_population(city, year):
    """ Import the population occupation numbers for the subdivisions (patches)
    or the given city or system. For certain places the year could be also
    a choice.

    Parameters
    ----------
    city : str
        Name of the city.
    year : str
        Year of the data.

    Returns
    -------
    pop_patch : array
        Every patch's population

    """

    lower_path = 'data/'
    full_path = os.path.join(path, lower_path)
    
    file_name = city + '_population'
    full_name = os.path.join(full_path, file_name + '.csv')

    patch_df = pd.read_csv(full_name)

    pop_patch = np.zeros(len(patch_df)-1, dtype=np.int_)
    pop_patch = patch_df[year].values.T[1:]

    return pop_patch


def get_mobility_scenario_dictionary(city):
    """
    Obtain the mobility scenario dictionary. It contains initial and final
    dates  in format YYYYMMDD for selected periods of time during the course of 
    mobility data recording. This periods maybe related to specific events
    on the mobility dynamics to the corresponding city.
    
    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    mob_dict : dict

    """

    mob_dict = {'ref': {'initial': '20200214', 'final': '20200220'},
                'ld1': {'initial': '20200315', 'final': '20200320'},
                'ld2': {'initial': '20200401', 'final': '20200409'},
                'ph1': {'initial': '20200511', 'final': '20200524'},
                'ph2': {'initial': '20200525', 'final': '20200607'},
                'ph3': {'initial': '20200608', 'final': '20200620'},
                'new': {'initial': '20200621', 'final': '20200727'},
                'wa3': {'initial': '20200915', 'final': '20201130'},
                'end': {'initial': '20210501', 'final': '20210509'}}
    
    return mob_dict
   

def import_mobility_date_dictionary(city):
    """
    Import the mobility dictionary for a given city ordered by dates.  

    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    mobility_date_dict : dict
        Number of travels among all patches in city for any registered date.

    """
    
    lower_path = 'data/'
    full_path = os.path.join(path, lower_path)
    
    name_prefix = city + '_travel_matrix_'
    file_name = name_prefix + 'all_days'
    
    full_name = os.path.join(full_path, file_name + '.pickle')
    
    mobility_date_dict = pk.load(open(full_name, "rb"))
    
    return mobility_date_dict
    

def build_averaged_travel_matrix(city, mob_id):
    """ 
    Build an average travel matrix. An entry of the travel matrix contains
    the number of travels between a pair of patches within a full day.  
    Initial and final dates are given and then the travel matrix for every day 
    within the period specified is added and averaged.

    Parameters
    ----------
    city : str
        Name of the city.
    mob_id : str
        Mobility scenario identifier.

    Returns
    -------
        : 2d float array 
        Average number of travels in a specified period between a pair of patches.

    """
    
    mob_scen_dict = get_mobility_scenario_dictionary(city)
    
    if city == 'ZARAGOZA':
        city_abb = 'zgz'
    elif city =='MADRID':
        city_abb = 'mad'
    else:
        city_abb = 'zgz'

    mob_date_dict = import_mobility_date_dictionary(city_abb)
    
    initial_date = mob_scen_dict[mob_id]['initial']
    final_date = mob_scen_dict[mob_id]['final']

    date_list = list(mob_date_dict.keys())
    V = len(mob_date_dict[date_list[0]])
     
    avg_travel_matrix = np.zeros((V, V), dtype=np.float_)
    
    initial_index = date_list.index(initial_date)
    final_index = date_list.index(final_date)
    
    index_range = final_index - initial_index + 1
    
    for index in range(0, index_range):
        
        date = date_list[index + initial_index]
        avg_travel_matrix += mob_date_dict[date]
        
    return avg_travel_matrix / index_range


def build_data_driven_diffusion_matrix(matrix, kappa):
    """
    Build a data driven diffusion matrix fed with a matrix of number
    of travels between a pair of patches. Off-diagonal matrix are coupled to
    a mobility parameter kappa to modulate the proportion of individuals
    outflowing a patch.
    
    Every element of the diffusion matrix gives the probability for an
    individual of traveling from an origin patch to a destination patch. Thus,
    the elements of every row should add up to unity.

    Parameters
    ----------
    matrix : 2d float array 
        Average number of travels in a specified period between a pair of patches.
    kappa : float
        Mobility parameter to scale with respect to reference mobility.

    Returns
    -------
    od_matrix : 2d float array
        Probability of reaching patch j from patch i (data-driven).

    """

    # Build rate matrix
    norm = np.sum(matrix, axis=1)
    dim = len(norm)
    od_matrix = np.zeros((dim, dim), dtype=np.float_)
    for ori in range(dim):
        for des in range(dim):
            if ori != des:
                od_matrix[ori][des] = kappa * matrix[ori][des] / norm[ori]
        od_matrix[ori][ori] = 1.0 - np.sum(od_matrix[ori])
        if od_matrix[ori][ori] <= 1.0e-15: # smash very low negative values
            od_matrix[ori][ori] = 0.0

    return od_matrix


def build_homogeneous_od_matrix(pop_patch, kappa):
    """
    Build an origin-destination matrix based on an homogeneous scheme.
    Every patch flow is equiprobable.
    
    Parameters
    ----------
    pop_patch : int array
        Every patch's population
    kappa : float
        Mobility parameter

    Returns
    -------
    od_matrix : 2d float array
        Probability of reaching patch j from patch i (data-driven).

    """
    
    V = len(pop_patch)
    
    value_ij = kappa / (V - 1)
    od_matrix = np.full((V, V), value_ij, dtype=np.float_)
    value_ii = 1.0 - value_ij * (V - 1)
    np.fill_diagonal(od_matrix, value_ii)

    return od_matrix


def build_proportional_od_matrix(pop_patch, kappa):
    """
    Build an origin-destination matrix based on proportional scheme.
    Every patch flow is proportional to the product of populations between
    origin & destination patches.

    Parameters
    ----------
    pop_patch : int array
        Every patch's population
    kappa : float
        Mobility parameter

    Returns
    -------
    od_matrix : 2d float array
        Probability of reaching patch j from patch i (data-driven).

    """
    
    popden_patch = pop_patch / np.sum(pop_patch)
    V = len(pop_patch)
    C = np.zeros(V, dtype=np.float_)
    od_matrix = np.zeros((V, V), dtype=np.float_)
    
    for ori in range(0, V):
        for des in range(0, V):
            if ori != des:
                C[ori] += popden_patch[ori] * popden_patch[des]

    for ori in range(0, V):
        for des in range(0, V):
            if ori != des:
                od_matrix[ori][des] = kappa * popden_patch[ori] * popden_patch[des] / C[ori]
        od_matrix[ori][ori] = 1.0 - np.sum(od_matrix[ori])
        if od_matrix[ori][ori] <= 1.0e-15:
            od_matrix[ori][ori] = 0.0

    return od_matrix


def renormalize_travel_matrix(matrix, pop_patch):
    
    V = len(pop_patch)
    
    new_matrix = np.zeros((V,V))
    
    for i in range(V):
        for j in range(V):
            term1 = matrix[i,j] * pop_patch[i] * pop_patch[i]
            term2 = matrix[j,i] * pop_patch[j] * pop_patch[j]
            new_matrix[i,j] = (term1 + term2) / (pop_patch[i] + pop_patch[j])
    
    return new_matrix


def import_mobility_data(city_abb):

    lower_path = 'data/'
    
    name_prefix = city_abb + '_travel_matrix_'

    day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                '31']
    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12']
    year_list = ['2020', '2021']
    
    travel_matrix_dict = {}
    total_travel_number_dict = {}

    for year in year_list:
    
        for month in month_list:
        
            for day in day_list:
            
                date = year + month + day
                
                file_name = name_prefix + date
                full_path = os.path.join(path, lower_path)
                full_name = os.path.join(full_path, file_name + '.csv')
                
                if os.path.exists(full_name):
                    
                    travel_matrix = pd.read_csv(full_name).to_numpy()
                    travel_matrix_dict[date] = travel_matrix
                    total_travel_number_dict[date] = np.sum(travel_matrix)
    
    file_name = name_prefix + 'all_days'
    full_name = os.path.join(full_path, file_name + '.pickle')
    pk.dump(travel_matrix_dict, open(full_name, "wb"))


def compute_mobility_observables(city_abb):
    
    lower_path = 'data'
    full_path = os.path.join(path, lower_path)
    
    name_prefix = city_abb + '_travel_matrix_'
    file_name = name_prefix + 'all_days'
    
    full_name = os.path.join(full_path, file_name + '.pickle')
    
    mobility_dict = pk.load(open(full_name, "rb"))
    
    day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                '31']
    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12']
    year_list = ['2020', '2021']
    
    dim_t = len(mobility_dict)
    dim_p = len(mobility_dict['20200214'])
    time_array = np.arange(dim_t)
    date_list = []
    weekday_list = []
    total_travel_array = np.zeros(dim_t)
    inter_patch_travel_array = np.zeros((dim_t, dim_p, dim_p))
    ori_total_travel_array = np.zeros((dim_t, dim_p))
    des_total_travel_array = np.zeros((dim_t, dim_p))
    outflow_patch_array = np.zeros((dim_t, dim_p))
    inflow_patch_array = np.zeros((dim_t, dim_p))
    inner_mobility_array = np.zeros((dim_t, dim_p))

    i = 0
    for year in year_list:
    
        for month in month_list:
        
            for day in day_list:
            
                date = year + month + day
                
                if date in mobility_dict.keys():
                    
                    weekday_list.append(relate_date_and_weekday(year, month, day))
                    date_list.append(date)
                    
                    travel_matrix = mobility_dict[date]
                    
                    total_travel_array[i] = np.sum(travel_matrix)
                    ori_total_travel_array[i,:] = np.sum(travel_matrix, axis=1)
                    des_total_travel_array[i,:] = np.sum(travel_matrix, axis=0)
                    inter_patch_travel_array[i,:] = travel_matrix
                    outflow_patch_array[i,:] = np.sum(travel_matrix, axis=1) \
                                                - np.diag(travel_matrix)
                    inflow_patch_array[i,:] = np.sum(travel_matrix, axis=0) \
                                                - np.diag(travel_matrix)
                    inner_mobility_array[i,:] = np.diag(travel_matrix)
                    
                    i = i + 1
    
    output = {}
    output['time'] = time_array
    output['date'] = date_list
    output['weekday'] = weekday_list
    output['total'] = total_travel_array
    output['inter'] = inter_patch_travel_array
    output['outflow'] = outflow_patch_array
    output['inflow'] = inflow_patch_array
    output['inner'] = inner_mobility_array
    output['ori_total'] = ori_total_travel_array
    output['des_total'] = des_total_travel_array

    return output


def relate_date_and_weekday(year, month, day):
    
    year = int(year)
    month = int(month)
    day = int(day)
         
    ans = datetime.date(year, month, day)
    return ans.strftime('%A')


def get_inter_patch_dict(results, dim_p):
    
    inter = results['inter']

    time_array = np.arange(len(inter))
    dim_t = len(time_array)
    
    inter_patch_dict = {p: [] for p in range(dim_p)}
    for i in range(dim_t):
        for patch in range(dim_p):
            inter_patch_dict[patch].append(inter[i][patch])
    
    return inter_patch_dict


def get_inflow_outflow_dict(results, dim_p):
    
    inflow = results['inflow']
    outflow = results['outflow']
    
    time_array = np.arange(len(inflow))
    dim_t = len(time_array)
    
    inflow_dict = {p: [] for p in range(dim_p)}
    outflow_dict = {p: [] for p in range(dim_p)}
    for i in range(dim_t):
        for patch in range(dim_p):
            inflow_dict[patch].append(inflow[i][patch])
            outflow_dict[patch].append(outflow[i][patch])
    
    return inflow_dict, outflow_dict


def get_inner_patch_dict(results, dim_p):
    
    inner = results['inner']

    time_array = np.arange(len(inner))
    dim_t = len(time_array)
    
    inner_patch_dict = {p: [] for p in range(dim_p)}
    for i in range(dim_t):
        for patch in range(dim_p):
            inner_patch_dict[patch].append(inner[i][patch])
    
    return inner_patch_dict


def unify_results(exp_id):
    
    import os
    import pickle as pk

    parent_wd = os.path.dirname(os.getcwd())

    i_path = os.path.join(parent_wd,'results/release/single_pickles/' + exp_id)
    o_path = os.path.join(parent_wd, 'results/release')

    files = os.listdir(i_path)

    results_dict = {}

    total_files = len(files)
    wrong = 0

    for file in files:

        if os.path.isfile(os.path.join(i_path, file)):

            try:
                input_data = open(os.path.join(i_path, file),'rb')
                results = pk.load(input_data)

                splitted_str = file.split('_', 4)
                theta = float(splitted_str[1])
                kappa = float(splitted_str[2])
                chi = float(splitted_str[3])

                key = (theta, kappa, chi)
                results_dict[key] = results[key]

            except:
                print('Wrong file:{0} \n'.format(file))
                wrong +1

    print('Successfully loaded files: {0}'.format(total_files - wrong))

    # Add control parameter keys
    tuple_keys_list = list(zip(*list(results_dict.keys())))
    results_dict['theta'] = sorted(list(set(tuple_keys_list[0])))
    results_dict['kappa'] = sorted(list(set(tuple_keys_list[1])))
    results_dict['chi'] = sorted(list(set(tuple_keys_list[2])))

    # Save unified results into pickle
    file_name = 'unified_' + splitted_str[0] + '_' + splitted_str[-1]
    full_name = os.path.join(o_path, file_name)
    output_file = open(full_name, 'wb')
    pk.dump(results_dict, output_file)
    output_file.close()


def generate_metadata_string(pars):
    
    metastring = ''
    
    for key, value in pars.items():
        new_item = '_' + str(key)[0:3] + str(value)
        metastring += new_item
        
    return metastring


def generate_baseline_string(city, patch_id, seeds, R0, nsims, T_MAX):

    pars = {}
    pars['city'] = city
    pars['patch_id'] = patch_id
    pars['mod_id'] = 'SIR'
    pars['mob_id'] = 'ref'
    pars['kappa'] = 1.0
    pars['seeds'] = seeds
    pars['R0'] = R0
    pars['T_I'] = 4.5
    pars['T_E'] = 2.5
    pars['nsims'] = nsims
    pars['T_MAX'] = T_MAX
    pars['theta'] = 1.0
    pars['chi'] = 1.0
    pars['epsilon'] = 1.0
    pars['hold'] = True

    metastring = ''
    
    for key, value in pars.items():
        new_item = '_' + str(key)[0:3] + str(value)
        metastring += new_item
        
    return metastring


def save_plot(path, filename, extension_list):
    """
    Save the plot as a file.
    
    Parameters
    ----------
    path : string
        Directory path.
    filename : string
        name of the file to be saved
    extension_list : string list
        list containing file extensions to save it
        
    Returns
    -------
    nothing
    
    """
    
    import matplotlib.pyplot as plt

    if not os.path.exists(path):
        os.makedirs(path)
    for ext in extension_list:
        fullName = os.path.join(path, filename + '.' + ext)
        plt.savefig(fullName, format=ext, bbox_inches='tight')
