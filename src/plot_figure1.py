#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 18:06:15 2022

@author: ademiguel
"""

import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_utils import save_plot


path = os.path.dirname(os.getcwd())
city_abb = 'mad'

lower_path = 'data'
full_path = os.path.join(path, lower_path)

file_name = city_abb + '_tia_last14d_bhz'
full_name = os.path.join(full_path, file_name + '.csv')

mad_tia_df = pd.read_csv(full_name)

#date_array = mad_tia_df['date'].values
week_array = mad_tia_df['x'].values
del mad_tia_df['Unnamed: 0']
#del mad_tia_df['date']
del mad_tia_df['x']
V = len(list(mad_tia_df.keys()))


locked_bhz_list = ['Chopera', 'Barajas', 'Alameda_de_Osuna', 'Puerta_Bonita',
                   'Vista_Alegre', 'Guayaba', 'Abrantes', 'Antonio_Leyva', 
                   'Comillas', 'Los_Cármenes', 'San_Isidro', 'Lavapiés', 
                   'Núñez_Morgado', 'Guzmán_el_Bueno', 'Andrés_Mellado',
                   'Eloy_Gonzalo', 'Doctor_Cirajas', 'Gandhi', 'Daroca', 
                   'La_Elipa', 'García_Noblejas', 'Jazmín', 'Mirasierra', 
                   'Las_Tablas', 'Virgen_de_Begoña', 'Sanchinarro', 
                   'Benita_de_Ávila', 'Silvano', 'Virgen_del_Cortijo', 
                   'Vicente_Muzas', 'Puerta_del_Ángel', 'General_Fanjul',
                   'Aravaca', 'Vinateros_Torito', 'Pavones', 'Vandel',
                   'Entrevías', 'Martínez_de_la_Riva', 'San Diego', 
                   'Numancia', 'Peña_Prieta', 'Pozo_de_Tío_Raimundo', 
                   'Ángela_Uriarte', 'Alcalá_de_Guadaíra', 'Federica_Montseny', 
                   'Campo_de_la_Paloma', 'Rafael_Alberti', 'Portazgo', 
                   'Montesa', 'General_Oráa', 'Baviera', 'Castelló', 'Alpes', 
                   'Rejas', 'Quinta_de_los_Molinos', 'General_Moscardó', 
                   'Infanta_Mercedes', 'Villaamil', 'Almendrales', 
                   'Las_Calesas', 'Zofío', 'Orcasur', 'San_Fermín', 
                   'Orcasitas', 'Vicálvaro_Artilleros', 'Valdebernardo', 
                   'Villa_de_Vallecas', 'San_Andrés', 'San_Cristóbal', 
                   'El_Espinillo','Los_Rosales', 'Alcocer']


cutoff_dates = ['2020/05/25', '2022/01/11']
cutoff_dates[0] = datetime.datetime(int(cutoff_dates[0][0:4]),
                                    int(cutoff_dates[0][5:7]),
                                    int(cutoff_dates[0][8:10]))
cutoff_dates[1] = datetime.datetime(int(cutoff_dates[1][0:4]),
                                    int(cutoff_dates[1][5:7]),
                                    int(cutoff_dates[1][8:10]))


start_date = cutoff_dates[0]
end_date   = cutoff_dates[1]

date_list = [start_date + datetime.timedelta(n) for n in range(int((end_date - start_date).days))]


# Prepare figure
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))


# LEFT FIGURE: LOCKED BHZs

# CHOPERA: Locked from 2021/04/05 until 2021/05/24
cir_t = mad_tia_df['Chopera']

locked_date = datetime.datetime(2021, 4, 5)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 24)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# BARAJAS: Locked from 2021/01/11 until 2021/02/15, then 2021/04/12 until 2021/05/24
cir_t = mad_tia_df['Barajas']

locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 15)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 12)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 5, 24)
free2_index = round(date_list.index(free2_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ALAMEDA DE OSUNA: Locked from 2021/01/11 until 2021/02/1, then 2021/04/05 until 2021/04/19
cir_t = mad_tia_df['Alameda_de_Osuna']

locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 1)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 5)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 4, 19)
free2_index = round(date_list.index(free2_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# PUERTA BONITA: Locked from 2020/09/21 until 2020/10/25
cir_t = mad_tia_df['Puerta_Bonita']

locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VISTA ALEGRE: Locked from 2020/09/21 until 2020/10/12
cir_t = mad_tia_df['Vista_Alegre']

locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GUAYABA: Locked from 2020/09/21 until 2020/10/12
cir_t = mad_tia_df['Guayaba']

locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ABRANTES: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['Abrantes']

locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ANTONIO LEYVA: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['Antonio_Leyva']

llocked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# COMILLAS: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['Comillas']

locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LOS CÁRMENES: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['Los_Cármenes']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SAN ISIDRO: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['San_Isidro']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LAVAPIÉS: Locked from 2020/10/12 until 2020/10/25
cir_t = mad_tia_df['Lavapiés']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# NÚÑEZ MORGADO: Locked from 2020/10/25 until 2020/11/20, then
cir_t = mad_tia_df['Núñez_Morgado']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 23)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 3, 22)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 4, 12)
free2_index = round(date_list.index(free2_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GUZMÁN EL BUENO: Locked from 2020/10/25 until 2020/12/14
cir_t = mad_tia_df['Guzmán_el_Bueno']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 12, 14)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ANDRÉS MELLADO: Locked from 2020/12/21 until 2021/03/21
cir_t = mad_tia_df['Andrés_Mellado']
locked_date = datetime.datetime(2020, 12, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 8)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ELOY GONZALO: Locked from 2021/04/19 until 2021/05/03
cir_t = mad_tia_df['Eloy_Gonzalo']
locked_date = datetime.datetime(2021, 4, 19)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 3)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# DOCTOR CIRAJAS: Locked from 2020/09/21 until 2020/12/07
cir_t = mad_tia_df['Doctor_Cirajas']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 12, 7)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GANDHI: Locked from 2020/09/21 until 2020/10/12, then 2021/04/26 until 2021/05/17
cir_t = mad_tia_df['Gandhi']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 26)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 5, 17)
free2_index = round(date_list.index(free2_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# DAROCA: Locked from 2020/09/21 until 2020/10/12, then 2021/04/26 until 2021/05/17
cir_t = mad_tia_df['Daroca']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2020, 10, 25)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2020, 12, 7)
free2_index = round(date_list.index(free2_date) / 7)

locked3_date = datetime.datetime(2021, 5, 3)
locked3_index = round(date_list.index(locked3_date) / 7)

free3_date = datetime.datetime(2021, 5, 24)
free3_index = round(date_list.index(free3_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:locked3_index+1], cir_t[free2_index:locked3_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked3_index:free3_index+1], cir_t[locked3_index:free3_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free3_index:], cir_t[free3_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LA ELIPA: Locked from 2020/09/21 until 2020/10/12, then 2020/11/23 until 2020/12/21
cir_t = mad_tia_df['Núñez_Morgado']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2020, 11, 23)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2020, 12, 21)
free2_index = round(date_list.index(free2_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GARCÍA NOBLEJAS
cir_t = mad_tia_df['García_Noblejas']
locked_date = datetime.datetime(2020, 9, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# JAZMÍN
cir_t = mad_tia_df['Jazmín']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# MIRASIERRA
cir_t = mad_tia_df['Mirasierra']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LAS TABLAS
cir_t = mad_tia_df['Las_Tablas']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 1)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VIRGEN DE BEGOÑA
cir_t = mad_tia_df['Virgen_de_Begoña']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 23)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 3, 22)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 4, 26)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SANCHINARRO
cir_t = mad_tia_df['Sanchinarro']
locked_date = datetime.datetime(2020, 12, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# BENITA DE ÁVILA
cir_t = mad_tia_df['Benita_de_Ávila']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 1)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SILVANO
cir_t = mad_tia_df['Silvano']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 15)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 12)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 5, 9)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)

# VIRGEN DEL CORTIJO
cir_t = mad_tia_df['Virgen_del_Cortijo']
locked_date = datetime.datetime(2021, 1, 4)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 2, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VICENTE MUZAS
cir_t = mad_tia_df['Vicente_Muzas']
locked_date = datetime.datetime(2021, 5, 3)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 17)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# PUERTA DEL ÁNGEL
cir_t = mad_tia_df['Puerta_del_Ángel']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 23)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GENERAL FANJUL
cir_t = mad_tia_df['General_Fanjul']
locked_date = datetime.datetime(2021, 4, 26)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 24)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ARAVACA
cir_t = mad_tia_df['Aravaca']
locked_date = datetime.datetime(2020, 12, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VINATEROS TORITO
cir_t = mad_tia_df['Vinateros_Torito']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 2, 22)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 3, 8)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# PAVONES
cir_t = mad_tia_df['Pavones']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VANDEL
cir_t = mad_tia_df['Vandel']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7 )

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ENTREVÍAS
cir_t = mad_tia_df['Entrevías']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# MARTÍNEZ DE LA RIVA
cir_t = mad_tia_df['Martínez_de_la_Riva']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SAN DIEGO
cir_t = mad_tia_df['San_Diego']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# NUMANCIA
cir_t = mad_tia_df['Numancia']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# PEÑA PRIETA
cir_t = mad_tia_df['Peña_Prieta']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# POZO DEL TÍO RAIMUNDO
cir_t = mad_tia_df['Pozo_de_Tío_Raimundo']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 20)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 2, 8)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 3, 15)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)



# ÁNGELA URIARTE
cir_t = mad_tia_df['Ángela_Uriarte']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ALCALÁ DE GUADAÍRA
cir_t = mad_tia_df['Alcalá_de_Guadaíra']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# FEDERICA MONTSENY
cir_t = mad_tia_df['Federica_Montseny']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# CAMPO DE LA PALOMA
cir_t = mad_tia_df['Campo_de_la_Paloma']
locked_date = datetime.datetime(2020, 9, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# RAFAEL ALBERTI
cir_t = mad_tia_df['Rafael_Alberti']
locked_date = datetime.datetime(2020, 9, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)



# PORTAZGO
cir_t = mad_tia_df['Portazgo']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)



# MONTESA
cir_t = mad_tia_df['Montesa']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GENERAL ORÁA
cir_t = mad_tia_df['General_Oráa']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 8)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# CASTELLÓ
cir_t = mad_tia_df['Castelló']
locked_date = datetime.datetime(2021, 4, 19)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 24)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)

# ALPES
cir_t = mad_tia_df['Alpes']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# REJAS
cir_t = mad_tia_df['Rejas']
locked_date = datetime.datetime(2021, 1, 11)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 5)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 5, 21)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# QUINTA DE LOS MOLINOS
cir_t = mad_tia_df['Quinta_de_los_Molinos']
locked_date = datetime.datetime(2021, 4, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 5, 3)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# GENERAL MOSCARDÓ
cir_t = mad_tia_df['General_Moscardó']
locked_date = datetime.datetime(2020, 12, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 3, 15)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# INFANTA MERCEDES
cir_t = mad_tia_df['Infanta_Mercedes']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VILLAAMIL
cir_t = mad_tia_df['Villaamil']
locked_date = datetime.datetime(2020, 10, 25)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 30)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ALMENDRALES
cir_t = mad_tia_df['Almendrales']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LAS CALESAS
cir_t = mad_tia_df['Las_Calesas']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ZOFÍO
cir_t = mad_tia_df['Zofío']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ORCASUR
cir_t = mad_tia_df['Orcasur']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SAN FERMÍN
cir_t = mad_tia_df['San_Fermín']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# ORCASITAS
cir_t = mad_tia_df['Orcasitas']
locked_date = datetime.datetime(2020, 9, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)



# VICÁLVARO-ARTILLEROS
cir_t = mad_tia_df['Vicálvaro_Artilleros']
locked_date = datetime.datetime(2020, 9, 28)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2020, 11, 23)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2020, 12, 7)
free2_index = round(date_list.index(free2_date) / 7)

locked3_date = datetime.datetime(2021, 3, 29)
locked3_index = round(date_list.index(locked3_date) / 7)

free3_date = datetime.datetime(2021, 4, 19)
free3_index = round(date_list.index(free3_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:locked3_index+1], cir_t[free2_index:locked3_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked3_index:free3_index+1], cir_t[locked3_index:free3_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free3_index:], cir_t[free3_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VALDEBERNARDO
cir_t = mad_tia_df['Valdebernardo']
locked_date = datetime.datetime(2021, 3, 29)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2021, 4, 26)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# VILLA DE VALLECAS
cir_t = mad_tia_df['Villa_Vallecas']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

locked2_date = datetime.datetime(2021, 4, 12)
locked2_index = round(date_list.index(locked2_date) / 7)

free2_date = datetime.datetime(2021, 5, 9)
free2_index = round(date_list.index(free2_date) / 7)


ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:locked2_index+1], cir_t[free_index:locked2_index+1],
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked2_index:free2_index+1], cir_t[locked2_index:free2_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free2_index:], cir_t[free2_index:], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SAN ANDRÉS
cir_t = mad_tia_df['San_Andrés']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# SAN CRISTÓBAL
cir_t = mad_tia_df['San_Cristóbal']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# EL ESPINILLO
cir_t = mad_tia_df['El_Espinillo']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 11, 16)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


# LOS ROSALES
cir_t = mad_tia_df['Los_Rosales']
locked_date = datetime.datetime(2020, 9, 21)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 12)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index], cir_t[0:locked_index], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)



# ALCOCER
cir_t = mad_tia_df['Alcocer']
locked_date = datetime.datetime(2020, 10, 12)
locked_index = round(date_list.index(locked_date) / 7)

free_date = datetime.datetime(2020, 10, 25)
free_index = round(date_list.index(free_date) / 7)

ax[0].plot(week_array[0:locked_index+1], cir_t[0:locked_index+1], 
        linestyle='solid', color='lightsteelblue', alpha=0.35)
ax[0].plot(week_array[locked_index-1:free_index+1], cir_t[locked_index-1:free_index+1],
        linestyle='solid', color='firebrick', alpha=0.35)
ax[0].plot(week_array[free_index:], cir_t[free_index:],
        linestyle='solid', color='lightsteelblue', alpha=0.35)


threshold_array = np.zeros(len(week_array))

threshold_array[0:17] = 0
threshold_array[17:20] = 1000
threshold_array[20] = 750
threshold_array[21:26] = 500
threshold_array[26:34] = 400
threshold_array[34] = 600
threshold_array[35:39] = 1000
threshold_array[39:41] = 500
threshold_array[41:43] = 400
threshold_array[43:47] = 350
threshold_array[47] = 400
threshold_array[48:51] = 500
threshold_array[51] = 400
threshold_array[52:] = 0

# PLS beginning, end & thresholds
ax[0].step(week_array, threshold_array, color='black', linestyle='dashed', alpha=1.0)
ax[0].axvline(x=17, color='black', linestyle='dashed', alpha=1.0)
ax[0].axvline(x=52, color='black', linestyle='dashed', alpha=1.0)

ax[0].text(70, 3900, 'A', fontsize=30, color='black', fontweight='bold', va='top')
ax[0].text(18, 3300, r'PLs start $\to$', fontsize=12, style='italic')
ax[0].text(18, 3500, '2020/9/21', fontsize=12, style='italic')
ax[0].text(53, 3000, '2021/5/21', fontsize=12, style='italic')
ax[0].text(53, 2800, r'PLs end', fontsize=12, style='italic')


# Plotting settings
#fig.suptitle('Real data evolution for locked BHZs')

ax[0].set_ylim(-100, 4000)

status_list = ['14-day CIR']

xtick_loc = [1, 15,  27, 40, 52, 66, 79]
labels = ['Jun 20', 'Sep 20', 'Dec 20', 'Mar 21', 'Jun 21', 'Sep 21', 'Dec 21']
ax[0].set_xticks(xtick_loc)
ax[0].set_xticklabels(ax[0].get_xticks(), rotation = 45)
ax[0].set_xticklabels(labels)

#ax[0].set_xlabel('weeks (since 2020/5/26)')    
ax[0].set_ylabel('{0}'.format(status_list[0]))
ax[0].yaxis.set_tick_params(right='on',which='both', direction='in', length=4)
#ax[0].xaxis.set_tick_params(right='on',which='both', direction='in', length=4)
#ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].grid(b=True, which='major', c='w', lw=2, ls='-')
#legend = ax[0].legend()
#legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax[0].spines[spine].set_visible(True)

# RIGHT FIGURE: FREE BHZs

for bhz in mad_tia_df.keys():
    if bhz not in locked_bhz_list:
        cir_t = mad_tia_df[bhz]
        ax[1].plot(week_array, cir_t, linestyle='solid', color='lightsteelblue', 
                   alpha=0.35)

ax[1].text(70, 3900, 'B', fontsize=30, color='black', fontweight='bold', va='top')
ax[1].text(18, 3300, r'PLs start $\to$', fontsize=12, style='italic')
ax[1].text(18, 3500, '2020/9/21', fontsize=12, style='italic')
ax[1].text(53, 3000, '2021/5/21', fontsize=12, style='italic')
ax[1].text(53, 2800, r'PLs end', fontsize=12, style='italic')

ax[1].step(week_array, threshold_array, color='black', linestyle='dashed', alpha=1.0)
ax[1].axvline(x=17, color='black', linestyle='dashed', alpha=0.7)
ax[1].axvline(x=52, color='black', linestyle='dashed', alpha=0.7)

# Plotting settings
ax[1].set_ylim(-100, 4000)
#ax[1].set_xlabel('weeks (since 2020/5/26)')
ax[1].set_xticks(xtick_loc)
ax[1].set_xticklabels(ax[1].get_xticks(), rotation = 45)
ax[1].set_xticklabels(labels)
ax[1].yaxis.set_tick_params(right='on',which='both', direction='in', length=4)
#ax[1].xaxis.set_tick_params(right='on',which='both', direction='in', length=4)
#ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].grid(b=True, which='major', c='w', lw=2, ls='-')
#legend = ax[1].legend()
#legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax[1].spines[spine].set_visible(True)

plt.rcParams.update({'font.size': 18})
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rcParams['pdf.fonttype'] = 42
    
lower_path = 'results'
full_path = os.path.join(path, lower_path)
base_name = 'figure1_bhzs' #+ metastring
save_plot(full_path, base_name, ['pdf', 'png'])


print('Yarimashita')