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

    def __init__(self, _data, _metadata, _yaxis_names, _country,
                 _regions, label=None, data_offset=4):
        self.data = _data
        self.metadata = _metadata
        self.yaxis_names = _yaxis_names
        self.country = _country
        self.regions = self.__setRegions(_regions)
        self.data_offset = data_offset
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
        self_available_regions = list(self.metadata[:, 1])
        self_selected_positions = common(self_available_regions, self.regions)[0]
        other_available_regions = list(other.metadata[:, 1])
        other_selected_positions = common(other_available_regions, other.regions)[0]
        (c_self, c_other) = common(self.yaxis_names,
                                   other.yaxis_names)
        self_data = self.data[:, c_self]
        other_data = other.data[:, c_other]
        _data = np.concatenate((self_data[self_selected_positions], other_data[other_selected_positions]))

        # (c_self, c_other) = common(self.yaxis_names[:self.data_offset],
        #                            other.yaxis_names[:other.data_offset])
        # self_metadata = self.metadata[:, c_self]
        # other_metadata = other.metadata[:, c_other]
        _metadata = np.concatenate((self.metadata[self_selected_positions], other.metadata[other_selected_positions]))

        (c_self, c_other) = common(self.yaxis_names,
                                   other.yaxis_names)
        _yaxis_names = list(np.array(self.yaxis_names)[c_self])
        _regions = self.regions + other.regions

        if self.label and other.label:
            _label = (self.label + '+' + other.label)
        elif self.label:
            _label = self.label
        elif other.label:
            _label = other.label
        else:
            _label = None

        return SIDS(_data, _metadata, _yaxis_names, '', _regions, _label)

    def timeline(self):
        return list(self.yaxis_names)

    def cases(self):
        available_regions = list(self.metadata[:, 1])
        selected_positions = common(available_regions, self.regions)[0]
        return self.data[selected_positions]

    def selectRegions(self, _regions, include_mainland=False):
        available_regions = list(self.metadata[:, 1])

        if include_mainland:
            try:
                _regions.append('')
            except AttributeError:
                _regions = ['']

        if not _regions:
            self.regions = available_regions
        else:
            c_regio = common(available_regions, _regions)[0]
            self.regions = list(np.array(available_regions)[c_regio])
            # self.data = self.data[c_regio]

    def show(self, lastN=None):
        objects = tuple(self.timeline())
        values = self.cases()

        if lastN:
            l = len(objects)
            objects = objects[l - lastN:]
            values = values[:, l - lastN:]

        y_pos = np.arange(len(objects))

        available_regions = list(self.metadata[:, 1])
        selected_positions = common(available_regions, self.regions)[0]
        selected_metadata = list(np.array(self.metadata)[selected_positions])

        for (regio, vals) in zip(selected_metadata, values):
            plt.plot(y_pos, vals, alpha=0.5, label=(regio[1] if regio[1] else regio[0]))
        plt.xticks(y_pos, objects, rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Infections')
        plt.legend()
        plt.title(self.label + ' . ' + self.country + ' infections')

        plt.show()
