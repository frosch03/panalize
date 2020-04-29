# -*- coding: utf-8 -*-
"""IDS - Infections Dataset

Filename   : IDS.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : An IDS - Infections Data Set - does contain data about
             confirmed infections on a larger scale. This could be the
             world with details per contry or a country with details
             on the regions.

"""

import numpy as np

from SIDS import SIDS
from HelperFunctions import genfromtxt_mod


class IDS:
    """Simple class to hold infection data for SARS-CoV-2"""

    def __init__(self, _filename, data_offset=4, pos_country=1, pos_region=0):
        self.filename = _filename
        self.data_offset = data_offset
        self.pos_country = pos_country
        self.pos_region = pos_region
        self.csvd = genfromtxt_mod(_filename, names=True, deletechars="", dtype=None, encoding=None)  # {}
        self.data = np.array(list(map(
            lambda data_line: np.asarray(list(data_line)[self.data_offset:]),
            self.csvd)))
        # metadata are per data line first the countries name and second the region name
        self.metadata = np.array(list(map(
            lambda data_line: np.asarray(list(data_line)[:self.data_offset]),
            self.csvd)))[:, [self.pos_country, self.pos_region]]

    def countryIdx(self, country):
        return list(self.metadata[:, 0]).index(country)

    def regions(self, country):
        return [x[1] for x in list(self.metadata) if x[0] == country]

    def regioIdxs(self, country):
        return [i for i, x in enumerate(list(self.metadata)) if x[0] == country]

    def __getitem__(self, country):
        rowIdx = self.countryIdx(country)
        _regions = self.regions(country)
        regioIdxs = self.regioIdxs(country)
        return SIDS(
            self.data[regioIdxs],
            self.metadata[regioIdxs],
            list(self.csvd[0].dtype.names)[self.data_offset:],
            country,
            _regions,
            data_offset=self.data_offset)
