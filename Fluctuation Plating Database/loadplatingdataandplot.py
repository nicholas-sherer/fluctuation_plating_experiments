#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:28:22 2018

@author: kuhlmanlab
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3 as sql

os.chdir('/home/kuhlmanlab/Documents/GitHub/')

import luriadelbruck as ldb

os.chdir('/home/kuhlmanlab/Documents/GitHub/Fluctuation Plating Database')

conn = sql.connect('fluctuation_plating_data.db')

all_platings = pd.read_sql_query('SELECT * from platings;', conn,
                                 parse_dates=['date'])

clean_platings = all_platings[(all_platings.lb_contam == 0) &
                              (all_platings.rif_contam == 0)]


NS001_saturated_iptg = \
    clean_platings[(clean_platings.strain == 'NS 001') &
                   (clean_platings.iptg == 2000)][['atc', 'lb', 'rif']]

mutation_rate_dict = {}

for atc in np.unique(NS001_saturated_iptg.atc):
    data = NS001_saturated_iptg[NS001_saturated_iptg.atc == atc][['lb', 'rif']].values
    lb = data[:, 0]*2.5*10**6
    rif = data[:, 1]
    sample_inference = ldb.SarkarMaSandri(rif, lb)
    mutation_rate = sample_inference.fit().params[0]
    mutation_rate_dict[atc] = mutation_rate

plt.loglog(.001+np.array(list(mutation_rate_dict.keys())), list(mutation_rate_dict.values()),'*')

print(mutation_rate_dict)
