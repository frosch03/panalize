"""HelperFunctions - Module containing a loose collection of helpfull
functions

Filename   : HelperFunctions.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : The module HelperFunctions contains a selection of helping
             functions

"""

import csv
import numpy as np


def genfromtxt_mod(fname, **kwargs):
    def rewrite_csv_as_tab(fname):
        with open(fname, 'r') as fp:
            rdr = csv.reader(fp)
            for row in rdr:
                yield '\t'.join(row)
    return np.genfromtxt(rewrite_csv_as_tab(fname), delimiter='\t', **kwargs)


def common(a, b):
    a_ret = [idx
             for idx, val
             in enumerate(a)
             if val in b]
    b_ret = [idx
             for idx, val
             in enumerate(b)
             if val in a]
    return (a_ret, b_ret)
