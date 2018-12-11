#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:51:37 2018

@author: kuhlmanlab

This file was used to generate the sql database of plating results. It probably
should have been split into an SQL file and then a separate python file for
inserting the data from February 7th to test the database, but it all worked in
the end anyways.
"""

import sqlite3
import os

# move to a directory to test making an SQL database
os.chdir('/home/kuhlmanlab/Documents/GitHub/Fluctuation Plating Database/')

# create database if file doesn't exist
conn = sqlite3.connect('fluctuation_plating_data.db')

# cursor is used to execute SQL statements
cursor = conn.cursor()

# SQL command to create a table of the e. coli strains
strain_table_creation = '''CREATE TABLE IF NOT EXISTS strains (
strain_id          INTEGER PRIMARY KEY,
strain_name        TEXT    NOT NULL UNIQUE,
strain_description TEXT    NOT NULL);'''

# SQL command to create a table of the media used to grow e. coli
medium_table_creation = '''CREATE TABLE IF NOT EXISTS media (
media_id          INTEGER  PRIMARY KEY,
media_name        TEXT     NOT NULL UNIQUE,
media_description TEXT     NOT NULL);'''

# SQL command to create a table of fluctuation plating protocols
protocol_table_creation = '''CREATE TABLE IF NOT EXISTS protocols (
protocol_id             INTEGER PRIMARY KEY,
protocol_name           TEXT    NOT NULL UNIQUE,
fraction_plated_inverse REAL    NOT NULL);'''

# SQL command to create the table used to store the results of experiments
plating_results_creation = '''CREATE TABLE IF NOT EXISTS platings (
date       TEXT     NOT NULL,
strain     TEXT     NOT NULL,
medium     TEXT     NOT NULL,
iptg       REAL     NOT NULL,
atc        REAL     NOT NULL,
lb         INTEGER  NOT NULL,
rif        INTEGER  NOT NULL,
lb_contam  INTEGER  NOT NULL,
rif_contam INTEGER  NOT NULL,
protocol   TEXT     NOT NULL,
    FOREIGN KEY (strain) REFERENCES strains(strain_name),
    FOREIGN KEY (medium) REFERENCES media(media_name),
    FOREIGN KEY (protocol) REFERENCES protocols(protocol_name)
);'''

plating_results_triggers = \
    '''CREATE TRIGGER valid_date BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (DATE(NEW.date) > DATE('NOW')) THEN
            RAISE (ABORT, 'Date later than today')
        END;
    END;
    CREATE TRIGGER valid_iptg BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.iptg < 0) THEN
            RAISE (ABORT, 'The iptg concentration must be nonnegative')
        END;
    END;
    CREATE TRIGGER valid_atc BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.atc < 0) THEN
            RAISE (ABORT, 'The atc concentration must be nonnegative')
        END;
    END;
    CREATE TRIGGER valid_lb BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.lb < 0 OR NEW.lb > 9999) THEN
            RAISE (ABORT, 'The number on lb must be from 0 to 9999')
        END;
    END;
    CREATE TRIGGER valid_rif BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.rif < 0 or NEW.rif > 9999) THEN
            RAISE (ABORT, 'The number on rif must be from 0 to 9999')
        END;
    END;
    CREATE TRIGGER valid_lb_contam BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.lb_contam < 0 or NEW.lb_contam > 9999) THEN
            RAISE (ABORT, 'The number of lb_contam must be from 0 to 9999')
        END;
    END;
    CREATE TRIGGER valid_rif_contam BEFORE INSERT ON platings
    BEGIN
        SELECT
        CASE WHEN (NEW.rif_contam < 0 or NEW.rif_contam > 9999) THEN
            RAISE (ABORT, 'The number of rif_contam must be from 0 to 9999')
        END;
    END;
    '''

# execute the SQL to create the tables
cursor.execute(strain_table_creation)
cursor.execute(medium_table_creation)
cursor.execute(protocol_table_creation)
cursor.execute(plating_results_creation)
cursor.executescript(plating_results_triggers)

# insert the protocol I use into the protocol table
insert_protocol = "INSERT INTO protocols VALUES (1, 'Sherer 2017', 2500000);"
cursor.execute(insert_protocol)

# insert elez's M9 medium into the media table
insert_M9_elez = '''INSERT INTO media VALUES (1, 'M9_elez',
'supplemented M9 medium from Elez and Matic et al');'''
cursor.execute(insert_M9_elez)

# the strains I've used so far in plating experiments
strains = [(1, 'MG1655', 'wild type e coli'),
           (2, 'MG1655 mCherry-mutH', 'MG1655 mCherry-mutH (native locus)'),
           (3, 'ME120', 'see Elez, Stoichiometry of MutS and MutL...'),
           (4, 'ME121', 'see Elez, Stoichiometry of MutS and MutL...'),
           (5, 'NS 001', '''ME121 Ptet-mCherry-mutH with lacI RBS Ptet-tetR at HK22 locus, pTKIP-Ptet-tetR''')]

# insert them into the strains table
cursor.executemany("INSERT INTO strains VALUES (?, ?, ?);", strains)

# commit all the changes to disk
conn.commit()

# next I want to insert some plating results, most of the values are duplicates
feb_7th_data = []
date = '2018-02-07'
strain = 'NS 001'
medium = 'M9_elez'
atc = 100
rif_cont = 0
protocol = 'Sherer 2017'

# the plate counts are what vary the most
iptg = [.01, .1, 1]
lb_p01 = [13, 15, 5, 7, 9, 14, 8, 9, 11, 10]
rif_p01 = [22, 63, 97, 39, 35, 115, 34, 70, 34, 113]
lb_p1 = [43, 44, 57, 35, 55, 39, 39, 41, 62, 27]
rif_p1 = [167, 106, 105, 193, 153, 175, 178, 93, 135, 210]
lb_1 = [8, 11, 13, 12, 10, 9, 16, 3, 5, 8]
rif_1 = [13, 12, 11, 31, 3, 13, 31, 32, 16, 12]

# loop over the plate counts and put everything into the feb_7th list of values
for i in range(10):
    if i == 2:
        lb_cont = 1
    else:
        lb_cont = 0
    value = (date, strain, medium, iptg[0], atc, lb_p01[i], rif_p01[i],
             lb_cont, rif_cont, protocol)
    feb_7th_data.append(value)

for i in range(10):
    lb_cont = 0
    value = (date, strain, medium, iptg[1], atc, lb_p1[i], rif_p1[i],
             lb_cont, rif_cont, protocol)
    feb_7th_data.append(value)

for i in range(10):
    lb_cont = 0
    value = (date, strain, medium, iptg[2], atc, lb_1[i], rif_1[i],
             lb_cont, rif_cont, protocol)
    feb_7th_data.append(value)

# insert the plating results from Feb. 7th into the SQL table
cursor.executemany('''INSERT INTO platings VALUES
                   (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', feb_7th_data)

# commit the changes
conn.commit()
