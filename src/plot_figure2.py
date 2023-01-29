#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 18:04:24 2022

@author: ademiguel
"""

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from data_utils import save_plot, compute_mobility_observables, get_inter_patch_dict


path = os.path.dirname(os.getcwd())


def plot_total_mobility(results):
    
    # Extract results
    total = results['total']
    weekday = results['weekday']
    time_array = np.arange(len(total) + 20)
    #print('time array {0}'.format(time_array))
    max_travels = np.max(total)
    total = total / max_travels

    # Build lists for different days
    sat_list = []
    total_sat = []
    sun_list = []
    total_sun = []
    weekdays_list = []
    total_weekdays = []
    
    for day, i in zip(weekday, range(len(weekday))):
        
        if day == 'Saturday':
            sat_list.append(time_array[i])
            total_sat.append(total[i])
        elif day == 'Sunday':
            sun_list.append(time_array[i])
            total_sun.append(total[i])
        else:
            weekdays_list.append(time_array[i])
            total_weekdays.append(total[i])

    # Prepare figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(weekdays_list, total_weekdays, linestyle='-', linewidth=0.75, 
            marker='o', markersize=1, color='lightsteelblue', label='Weekdays')
    ax.plot(sat_list, total_sat, linestyle='-', linewidth=0.75,
            marker='o', markersize=1, color='lightskyblue', label='Sat')
    ax.plot(sun_list, total_sun, linestyle='-', linewidth=0.75, 
            marker='o', markersize=1, color='dodgerblue', label='Sun')

    # Plot COVID-19 waves approximate period
    date_list = results['date']
    
    # Mark relevant events during the epidemic evolution
    t = date_list.index('20200315') # ESTADO DE ALARMA
    ax.axvline(x=t, color='crimson', alpha=1.0)
    ax.text(32, 0.1, 'National lockdown', fontsize=8, color='black', fontweight='bold', va='top')
    
    #t = date_list.index('20200328') # TIGHTENING
    #ax.axvline(x=t, color='crimson', alpha=1.0)
    #ax.text(42, 0.1, 'B', fontsize=10, color='black', fontweight='bold', va='top')
    
    #t = date_list.index('20200409') #
    #ax.axvline(x=t, color='indigo', linestyle='dashed', alpha=1.0)
    #ax.text(60, 0.1, 'C', fontsize=10, color='black', fontweight='bold', va='top')
    
    #t = date_list.index('20200511') # RELEASE: PHASE 1
    #ax.axvline(x=t, color='indigo', linestyle='dashed', alpha=1.0)
    #ax.text(90, 0.1, 'D', fontsize=10, color='black', fontweight='bold', va='top')
    
    #t = date_list.index('20200621') # RELEASE: NUEVA NORMALIDAD
    #ax.axvline(x=t, color='indigo', linestyle='dashed', alpha=1.0)
    #ax.text(130, 0.1, 'E', fontsize=10, color='black', fontweight='bold', va='top')
    
    t = date_list.index('20200921') # PLS STARTS
    index = weekdays_list.index(t)
    print(total[t] / total[0])
    ax.axvline(x=t, color='crimson', alpha=1.0)
    ax.text(225, 0.1, '', fontsize=10, color='black', fontweight='bold', va='top')
    ax.text(225, 0.9, '2020/9/21', style='italic', fontsize=10)
    ax.text(225, 0.85, r'PLs start $\longrightarrow$', style='italic', fontsize=10)
    
    t_end = 467 # PLS ENDS
    #index = weekdays_list.index(t)
    ax.axvline(x=t_end, color='indigo', linestyle='dashed', alpha=1.0)
    ax.text(390, 0.1, '', fontsize=10, color='black', fontweight='bold', va='top')
    ax.text(390, 0.9, '2021/5/21', style='italic', fontsize=10)
    ax.text(390, 0.85, r'PLs end', style='italic', fontsize=10)
    
    # Extract some mobility levels
    print("Mobility level for the first two weeks after PLS")
    z = 1.96
    n = len(total_weekdays[index:index+10])
    avg_pls_2w_wd = np.mean(total_weekdays[index:index+10])
    std_pls_2w_wd = np.std(total_weekdays[index:index+10])
    l95_pls_2w_wd = avg_pls_2w_wd - (z * std_pls_2w_wd / np.sqrt(n))
    u95_pls_2w_wd = avg_pls_2w_wd + (z * std_pls_2w_wd / np.sqrt(n))
    
    print("Weekdays only: {0} [{1},{2}]".format(avg_pls_2w_wd, l95_pls_2w_wd, 
                                                u95_pls_2w_wd))
    
    n = len(total[t:t+14])
    avg_pls_2w_t = np.mean(total[t:t+14])
    std_pls_2w_t = np.std(total[t:t+14])
    l95_pls_2w_t = avg_pls_2w_t - (z * std_pls_2w_t / np.sqrt(n))
    u95_pls_2w_t = avg_pls_2w_t + (z * std_pls_2w_t / np.sqrt(n))
    
    print("Total: {0} [{1},{2}]".format(avg_pls_2w_t, l95_pls_2w_t, 
                                                u95_pls_2w_t))
    
    print("Mobility level for the PLS period")
    n = len(total_weekdays[index:])
    avg_pls_t_wd = np.mean(total_weekdays[index:])
    std_pls_t_wd = np.std(total_weekdays[index:])
    l95_pls_t_wd = avg_pls_t_wd - (z * std_pls_t_wd / np.sqrt(n))
    u95_pls_t_wd = avg_pls_t_wd + (z * std_pls_t_wd / np.sqrt(n))
    
    print("Weekdays only: {0} [{1},{2}]".format(avg_pls_t_wd, l95_pls_t_wd, 
                                                u95_pls_t_wd))
    
    n = len(total[t:])
    avg_pls_t_t = np.mean(total[t:])
    std_pls_t_t = np.std(total[t:])
    l95_pls_t_t = avg_pls_t_t - (z * std_pls_t_t / np.sqrt(n))
    u95_pls_t_t = avg_pls_t_t + (z * std_pls_t_t / np.sqrt(n))
    
    print("Total: {0} [{1},{2}]".format(avg_pls_t_t, l95_pls_t_t, 
                                                u95_pls_t_t))
    
    #xticks = np.arange(0, 500, 30)
    #ax.set_xticks(xticks)
    xtick_loc = [date_list.index('20200301'), date_list.index('20200401'), 
                 date_list.index('20200501'), date_list.index('20200601'),
                 date_list.index('20200701'), date_list.index('20200801'),
                 date_list.index('20200901'), date_list.index('20201001'),
                 date_list.index('20201101'), date_list.index('20201201'),
                 date_list.index('20210101'), date_list.index('20210201'),
                 date_list.index('20210301'), date_list.index('20210401'),
                 date_list.index('20210501')]
    ax.set_xticks(xtick_loc)
    ax.set_xticklabels(ax.get_xticks(), rotation = 45)
    labels = ['Mar 20', 'Apr 20', 'May 20', 'Jun 20', 'Jul 20',
              'Aug 20', 'Sep 20', 'Oct 20', 'Nov 20', 'Dec 20', 'Jan 21',
              'Feb 21', 'Mar 21', 'Apr 21', 'May 21']
    ax.set_xticklabels(labels)

    ax.set_xlim([-20, np.max(time_array)+10])
    ax.set_ylim(0, 1.0)

    ax.set_ylabel('normalized number of travels')
    #ax.set_xlabel('day (since 2020/2/14)')
    
    minor_locator = AutoMinorLocator(2)
    ax.yaxis.set_minor_locator(minor_locator)
    #ax.grid(which='minor')
    
    legend = ax.legend(loc=4, prop={'size': 10})
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(True)
    
    plt.rcParams.update({'font.size': 14})
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42

    lower_path = 'results/'
    full_path = os.path.join(path, lower_path)
    base_name = 'figure2_mobility'
    save_plot(full_path, base_name, ['pdf', 'png'])


mob_dict = compute_mobility_observables('mad')
plot_total_mobility(mob_dict)

