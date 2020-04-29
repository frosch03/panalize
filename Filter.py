# -*- coding: utf-8 -*-
"""Filter - which can be applied onto infection data

Filename   : Filter.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : Filter to calculate:
             - dailyNew :: substracts the predecessor from each value to in order
               to get the daily new infections

|----.----|----.----|----.----|----.----|----.----|----.----|----.----I----.----|
"""

import numpy as np
from SIDS import SIDS


def dailyNew(il):
    return applyOnInfectionline(np.diff, il)

def applyOnInfectionline(fn, il, label="unknown"):
    new_cases = fn(il.cases())
    delta_length = len(il.cases()[0]) - len(new_cases[0])
    new_timeline = il.timeline()[delta_length:]
    new_data = new_cases
    new_csv_names = il.csv_names[:il.offset] + new_timeline
    if il.label:
        new_label = label + il.label
    else:
        new_label = label
    return SIDS(new_data,
                il.metadata,
                new_yaxis_names,
                il.country,
                il.regions,
                label=new_label,
                _offset=il.offset)
