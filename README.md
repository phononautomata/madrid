# MADRID

## Introduction
This repository contains the minimal code for the simulations in the manuscript: 
"Assessing the effectiveness of perimeter lockdowns as a response to epidemics at the urban scale: the case of Madrid" (under peer-review)

In this paper we built an epidemiological SIR metapopulation model with the ability to implement perimeter lockdowns, inspired by the case of Madrid, 
Spain, during September 2020. As such, our metapopulation model consists of 21 subpopulations, the official administrative regions of the city of Madrid,
and the mobility model connecting those subpopulations is informed with real mobility flows from the city based on a reference period during February 2020.
A standard SIR epidemic dynamics is run at every subpopulation. A risk threshold set, so that whenever the 14-day cumulative incidence rate is surpassed
locally (in a certain district), mobility in-and-out of the affected area is totally banned, and also some further transmission reduction is achieved
within. This behavioral response tries to emulate the strategy followed by Madrid's health authories during the aforementioned period of the COVID-19
epidemic.

The code hosted here is minimal because it contains the data and the model used for the manuscript's main results, but at the moment some pipeflow scripts 
for organizing the simulations output and plotting routines lack (hopefully, I will upload them after tidying them up). Apart from the basic model and 
related utilies, the scripts for figure 1 and figure 2 in the manuscript are present, and also a basic example and plotting scripts that allows the user to 
explore the system's global dynamics.

## Setup 
The model requires the basic standard packages such as [NumPy](https://numpy.org) and [Pandas](https://pandas.pydata.org). It also requires [Pickle](https://docs.python.org/3/library/pickle.html) for output results storage and input data for some plots, and [datetime](https://docs.python.org/3/library/datetime.html).

## Basic Usage
Assuming all the required packages are correctly installed, and the full madrid directory (subdirectories and files) has been downloaded in the home folder, then you can execute the example script by typing:

```

python ~/madrid/src example.py

```

Model parameters can be modified within the script.

In a similar fashion, you can launch plot_figure1.py and plot_figure2.py scripts:

```

python ~/madrid/src plot_figure1.py

```

```

python ~/madrid/src plot_figure2.py

```

## Data
The metapopulation model uses real data for populating the patches in the system and for informing the mobility flows. The population data can be found [here](https://github.com/phononautomata/madrid/blob/master/data/madrid_population.csv). The left column represents Madrid's administrative district and the right column represents 2020 population. The mobility data in human-readable format can be found [here](https://github.com/phononautomata/madrid/blob/master/data/0000_referencia_maestra1_mitma_distrito/mad_ref_week_travel_matrix.csv). This is a 21x21 table, where element (ij) represents the average total number of travels between district i and district j in the reference period (Feb 2020). This mobility data has been obtained through an R script (found [here](https://github.com/phononautomata/madrid/blob/master/src/mad_curate_mob_data.R)). Inside, the script you can find a more detailed description of the curation process.   

## Upgrades
In the future I hope to give a more friendly-user version of the model together with more features.
