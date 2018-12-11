#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:00:48 2018

@author: kuhlmanlab

This file has some convenience functions for inserting new plating results into
my tiny SQL database of results of e. coli platings.
"""

import sqlite3
import os


def format_for_db(date, strain, medium, iptg, atc, protocol, lb, rif,
                  lb_contam=None, rif_contam=None, cAMP=0):
    values_to_add = []
    if lb_contam is None:
        lb_contam = {}
    if rif_contam is None:
        rif_contam = {}
    for i in range(len(lb)):
        try:
            lb_cont = lb_contam[i]
        except KeyError:
            lb_cont = 0
        try:
            rif_cont = rif_contam[i]
        except KeyError:
            rif_cont = 0
        value = (date, strain, medium, iptg, atc, int(lb[i]), int(rif[i]),
                 int(lb_cont), int(rif_cont), protocol, cAMP)
        values_to_add.append(value)
    return values_to_add


def insert_to_db(values, database_file, directory=None):
    if directory is not None:
        os.chdir(directory)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    try:
        cursor.executemany("""INSERT INTO platings VALUES
                           (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", values)
    except sqlite3.IntegrityError as e:
        print(e)
        conn.close()
        return
    conn.commit()
    conn.close()
