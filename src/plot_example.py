import os
import numpy as np
import matplotlib.pyplot as plt

import analysis as an
import data_utils as du

path = os.path.dirname(os.getcwd())
lower_path = 'results/'


def plot_global_dynamics(global_ost, pars):

    # Load relevant data
    print("hold it!")

    # Prepare figure
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)

    # Extract observables
    I_st = global_ost['I']
    R_st = global_ost['R']
    Rtg_st = global_ost['Rt_g']
    N = global_ost['N'][0]
    
    i_t_dict = an.extract_time_series_statistics(I_st)
    r_t_dict = an.extract_time_series_statistics(R_st)
    Rtg_dict = an.extract_time_series_statistics(Rtg_st)
    time = range(0, len(global_ost['S'][0]))
    
    if pars['stat'] == 'avg':
    
        i_t_main = i_t_dict['avg'] / N
        i_t_lower = i_t_dict['l95'] / N
        i_t_upper = i_t_dict['u95'] / N
    
        r_t_main = r_t_dict['avg'] / N
        r_t_lower = r_t_dict['l95'] / N
        r_t_upper = r_t_dict['u95'] / N

        Rtg_t_main = Rtg_dict['avg']
        Rtg_lower = Rtg_dict['l95']
        Rtg_upper = Rtg_dict['u95']

    elif pars['stat'] == 'med':
    
        i_t_main = i_t_dict['med'] / N
        i_t_lower = i_t_dict['p05'] / N
        i_t_upper = i_t_dict['p95'] / N
    
        r_t_main = r_t_dict['med'] / N
        r_t_lower = r_t_dict['p05'] / N
        r_t_upper = r_t_dict['p95'] / N

        Rtg_t_main = Rtg_dict['med']
        Rtg_lower = Rtg_dict['p05']
        Rtg_upper = Rtg_dict['p95']

    # Plot main statistic time series for both scenarios
    ax.plot(time, i_t_main, linestyle='solid', color='dodgerblue', alpha=1.0)
    ax.plot(time, r_t_main, linestyle='solid', color='firebrick', alpha=1.0)
    ax_r = ax.twinx()
    ax_r.plot(time, Rtg_t_main, linestyle='dashed', color='black', alpha=0.8)
    
    # Plot deviation time series for both scenarios
    ax.fill_between(time, i_t_lower, i_t_upper, color='royalblue', alpha=0.3)
    ax.fill_between(time, r_t_lower, r_t_upper, color='lightcoral', alpha=0.3)
    ax.fill_between(time, r_t_lower, r_t_upper, color='silver', alpha=0.3)

    # Plot original R0 line and Rt=1 line
    R0 = pars['R0']
    ax_r.hlines(y=R0, xmin=np.min(time), xmax=np.max(time), linestyle='dashed', color='grey')
    ax_r.hlines(y=1, xmin=np.min(time), xmax=np.max(time), linestyle='dashed', color='teal')

    # Settings
    ax.set_title('Example of dynamical trajectories')
    ax.set_ylabel('normalized global population')
    ax.set_xlabel('time (days)')
    ax_r.set_ylabel(r'$R_t$')
    ax_r.set_ylim(0.0, np.max(Rtg_upper) + 1)

    # Font & font sizes
    plt.rcParams.update({'font.size': 15})
    plt.rc('axes', labelsize=20) 
    plt.rcParams['xtick.labelsize'] = 20
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42
    
    # Save plot
    full_path = os.path.join(path, lower_path)
    metastring = du.generate_metadata_string(pars)
    base_name = 'globaldyn_' + metastring
    extension_list = ['pdf', 'png']
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    for ext in extension_list:
        full_name = os.path.join(full_path, base_name + '.' + ext)
        plt.savefig(full_name, format=ext, bbox_inches='tight')
    plt.show()