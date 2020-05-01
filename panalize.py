# -*- coding: utf-8 -*-
"""Panalize - a simple script to draw infection data into diagrams

Filename   : panalize.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : Read the data from the CSSE dataset of the Johns Hopkins
             University. The dataset is distributed via git [1].

             [1] https://github.com/CSSEGISandData/COVID-19.git
"""

DATASET = "/home/frosch03/Programming/DataSets/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"  # noqa
US_DATASET = "/home/frosch03/Programming/DataSets/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"  # noqa

from IDS import IDS
from Filter import dailyNew

world = IDS(DATASET)
de = world['Germany']
fr = world['France']
fr.selectRegions([], include_mainland=True)
es = world['Spain']
it = world['Italy']
cn = world['China']
cn.selectRegions(['Hubei'])

us = IDS(US_DATASET, data_offset=11, pos_country=6, pos_region=5)
ny = us['New York']
ny.selectRegions(['New York'])

""" 
One can now show the cummulated infection count of one of the above
defined countries like so:

>>> de.show()

The daily new infections graph can be showed via:

>>> dailyNew(de).show()

As SIDS can be added together, the graph of multiple countries can
created via:

>>> (de + fr + es + it + cn).show()

Again the filter function can be applied so that the countries daily
new infections can be calculated via:

>>> (de + fr + es + it + cn).show()
"""
