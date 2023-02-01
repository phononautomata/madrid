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
The model requires basic standard packages as [NumPy](https://numpy.org). It also requires [Pickle](https://docs.python.org/3/library/pickle.html) for output results storage and input data for some plots.

# Basic Usage

# Examples 

# License
[MIT]
