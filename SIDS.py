# -*- coding: utf-8 -*-
"""SIDS - Specific Infections Dataset

Filename   : SIDS.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : An SIDS - Specific Infections Data Set - does contain data
             about confirmed infections limited to a specific set of
             infections data.

"""

import numpy as np
import matplotlib.pyplot as plt

from HelperFunctions import common


class SIDS:
    """Simple class to hold infection data per defined regions for
       SARS-CoV-2"""

    def __init__(self, _data, _metadata, _csv_names, _country,
                 _regions, label=None, _offset=4):
        self.data = _data
        self.metadata = _metadata
        self.csv_names = _csv_names
        self.country = _country
        self.regions = self.__setRegions(_regions)
        self.offset = _offset
        if not label:
            self.label = ""
        else:
            self.label = label

    def __setRegions(self, _regions):
        return list(map(lambda x: x if x else self.country,
                        _regions))

    def __dateIdx(self, datestring):
        return self.csv_names.dtype.names[self.offset:].index(datestring)

    def __getitem__(self, index):
        return self.data[:, self.__dateIdx(index)]

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __add__(self, other):
        if self.csv_names[:self.offset] != other.csv_names[:other.offset]:
            raise Exception('Differing csv layout within InfectionLines')

        (c_self, c_other) = common(self.csv_names[self.offset:],
                                   other.csv_names[other.offset:])
        self_data = self.data[:, c_self]
        other_data = other.data[:, c_other]
        _data = np.concatenate((self_data, other_data))

        (c_self, c_other) = common(self.csv_names[:self.offset],
                                   other.csv_names[:other.offset])
        self_metadata = self.metadata[:, c_self]
        other_metadata = other.metadata[:, c_other]
        _metadata = np.concatenate((self_metadata, other_metadata))

        (c_self, c_other) = common(self.csv_names,
                                   other.csv_names)
        _csv_names = list(np.array(self.csv_names)[c_self])
        _regions = self.regions + other.regions

        if self.label and other.label:
            _label = (self.label + '+' + other.label)
        elif self.label:
            _label = self.label
        elif other.label:
            _label = other.label
        else:
            _label = None

        return SIDS(_data, _metadata, _csv_names, '', _regions, _label)

    def timeline(self):
        return list(self.csv_names)[self.offset:]

    def cases(self):
        available_regions = list(self.metadata[:, 1])
        selected_positions = common(available_regions, self.regions)[0]
        return self.data[selected_positions]


    def setRegions(self, _regions):
        _regions.append('')
        c_regio = common(self.regions, _regions)[0]
        self.regions = list(np.array(self.regions)[c_regio])
        self.data = self.data[c_regio]

    def show(self, lastN=None):
        objects = tuple(self.timeline())
        values = self.cases()

        if lastN:
            l = len(objects)
            objects = objects[l - lastN:]
            values = values[:, l - lastN:]

        y_pos = np.arange(len(objects))

        for (regio, vals) in zip(self.regions, values):
            plt.plot(y_pos, vals, alpha=0.5, label=regio)
        plt.xticks(y_pos, objects, rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Infections')
        plt.legend()
        plt.title(self.label + ' . ' + self.country + ' infections')

        plt.show()
